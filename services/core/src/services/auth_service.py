from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..models import Session, User
from ..plugins import event_bus
from ..schemas.token import Token, TokenPayload
from ..schemas.user import UserCreate
from ..utils.email import send_email
from ..utils.security import generate_random_token, hash_password, verify_password

_reset_tokens: dict[str, str] = {}  # token -> user_id (dev; em prod usar Redis com TTL)
_verify_tokens: dict[str, str] = {}


async def register_user(db: AsyncSession, data: UserCreate) -> User:
    exists = (await db.execute(select(User).where(User.email == data.email))).scalar_one_or_none()
    if exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email já registado")
    user = User(**data.model_dump(exclude={"password"}), password_hash=hash_password(data.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    token = generate_random_token(16)
    _verify_tokens[token] = user.id
    await send_email(user.email, "Confirme o seu email", "verify_email", {"token": token})
    await event_bus.publish("auth.user.registered", {
        "user_id": user.id, "email": user.email, "role": user.role.value, "institution_id": user.institution_id,
    })
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    user = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciais inválidas")
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Conta desactivada")
    user.last_login = datetime.now(timezone.utc)
    await db.commit()
    return user


def create_access_token(user: User, jti: str) -> tuple[str, int]:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user.id, "jti": jti, "role": user.role.value, "institution_id": user.institution_id,
               "exp": exp, "type": "access"}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM), settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60


def create_refresh_token() -> str:
    return generate_random_token(48)


async def issue_tokens(db: AsyncSession, user: User, ip: str | None = None, ua: str | None = None) -> Token:
    jti = generate_random_token(16)
    access, expires_in = create_access_token(user, jti)
    refresh = create_refresh_token()
    db.add(Session(
        user_id=user.id, token=jti, refresh_token=refresh, ip_address=ip, user_agent=(ua or "")[:500],
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    ))
    await db.commit()
    await event_bus.publish("auth.user.logged_in", {"user_id": user.id, "ip": ip})
    return Token(access_token=access, refresh_token=refresh, expires_in=expires_in)


def verify_token(token: str) -> TokenPayload:
    try:
        return TokenPayload(**jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]))
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token inválido ou expirado",
                            headers={"WWW-Authenticate": "Bearer"})


async def refresh_tokens(db: AsyncSession, refresh_token: str) -> Token:
    sess = (await db.execute(select(Session).where(Session.refresh_token == refresh_token))).scalar_one_or_none()
    now = datetime.now(timezone.utc)
    if not sess or sess.revoked_at or sess.expires_at.replace(tzinfo=timezone.utc) < now:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Refresh token inválido")
    sess.revoked_at = now  # rotação
    user = await db.get(User, sess.user_id)
    return await issue_tokens(db, user, sess.ip_address, sess.user_agent)


async def revoke_token(db: AsyncSession, jti: str) -> None:
    sess = (await db.execute(select(Session).where(Session.token == jti))).scalar_one_or_none()
    if sess:
        sess.revoked_at = datetime.now(timezone.utc)
        await db.commit()


async def is_revoked(db: AsyncSession, jti: str) -> bool:
    sess = (await db.execute(select(Session).where(Session.token == jti))).scalar_one_or_none()
    return bool(sess and sess.revoked_at)


async def forgot_password(db: AsyncSession, email: str) -> None:
    user = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    if user:  # resposta idêntica quer exista quer não (anti-enumeração)
        token = generate_random_token(24)
        _reset_tokens[token] = user.id
        await send_email(email, "Recuperação de palavra-passe", "reset_password", {"token": token})


async def reset_password(db: AsyncSession, token: str, new_password: str) -> None:
    user_id = _reset_tokens.pop(token, None)
    if not user_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Token inválido")
    user = await db.get(User, user_id)
    user.password_hash = hash_password(new_password)
    await db.commit()
    await event_bus.publish("auth.password.reset", {"user_id": user.id})


async def verify_email(db: AsyncSession, token: str) -> None:
    user_id = _verify_tokens.pop(token, None)
    if not user_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Token inválido")
    user = await db.get(User, user_id)
    user.is_verified = True
    await db.commit()
    await event_bus.publish("auth.user.verified", {"user_id": user.id})


async def change_password(db: AsyncSession, user: User, current: str, new: str) -> None:
    if not verify_password(current, user.password_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Palavra-passe actual incorrecta")
    user.password_hash = hash_password(new)
    await db.commit()
