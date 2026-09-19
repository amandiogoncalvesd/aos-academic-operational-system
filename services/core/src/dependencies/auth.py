from collections.abc import Iterable
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from ..config import settings
from ..models import Role, User, UserRole
from ..services import auth_service
from .database import DB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")


async def get_current_user(request: Request, db: DB, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    payload = auth_service.verify_token(token)
    if payload.type != "access" or await auth_service.is_revoked(db, payload.jti):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Sessão terminada")
    user = await db.get(User, payload.sub)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Utilizador não existe")
    request.state.user_id, request.state.jti = user.id, payload.jti
    return user


async def get_current_active_user(user: Annotated[User, Depends(get_current_user)]) -> User:
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Conta desactivada")
    return user


CurrentUser = Annotated[User, Depends(get_current_active_user)]


def require_role(*roles: UserRole | str):
    allowed = {r.value if isinstance(r, UserRole) else r for r in roles}

    async def dep(user: CurrentUser) -> User:
        if user.role.value not in allowed and user.role != UserRole.admin:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Sem permissão para esta operação")
        return user
    return Depends(dep)


def require_permission(resource: str, action: str):
    code = f"{resource}.{action}"

    async def dep(user: CurrentUser, db: DB) -> User:
        if user.role == UserRole.admin:
            return user
        roles: Iterable[Role] = (await db.execute(select(Role).where(Role.name == user.role.value))).scalars().all()
        perms = {p for r in roles for p in (r.permissions or [])}
        if code not in perms and f"{resource}.*" not in perms and "*" not in perms:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Permissão em falta: {code}")
        return user
    return Depends(dep)


AdminUser = Annotated[User, require_role(UserRole.admin)]
