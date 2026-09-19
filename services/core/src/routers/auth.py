from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies.auth import CurrentUser
from ..dependencies.database import DB
from ..dependencies.rate_limit import AUTH_LIMIT, limiter
from ..schemas import (ForgotPassword, RefreshToken, SuccessResponse, Token, UserCreate, UserLogin,
                       UserPasswordChange, UserPasswordReset, UserResponse, UserUpdate)
from ..services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(AUTH_LIMIT)
async def register(request: Request, data: UserCreate, db: DB):
    return await auth_service.register_user(db, data)


@router.post("/login", response_model=Token)
@limiter.limit(AUTH_LIMIT)
async def login(request: Request, db: DB, form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Login OAuth2 (form: username=email, password)."""
    user = await auth_service.authenticate_user(db, form.username, form.password)
    return await auth_service.issue_tokens(db, user, request.client.host if request.client else None,
                                           request.headers.get("user-agent"))


@router.post("/login/json", response_model=Token)
@limiter.limit(AUTH_LIMIT)
async def login_json(request: Request, data: UserLogin, db: DB):
    user = await auth_service.authenticate_user(db, data.email, data.password)
    return await auth_service.issue_tokens(db, user, request.client.host if request.client else None,
                                           request.headers.get("user-agent"))


@router.post("/refresh", response_model=Token)
async def refresh(data: RefreshToken, db: DB):
    return await auth_service.refresh_tokens(db, data.refresh_token)


@router.post("/logout", response_model=SuccessResponse)
async def logout(request: Request, user: CurrentUser, db: DB):
    await auth_service.revoke_token(db, request.state.jti)
    return SuccessResponse(message="Sessão terminada")


@router.post("/forgot-password", response_model=SuccessResponse)
@limiter.limit(AUTH_LIMIT)
async def forgot_password(request: Request, data: ForgotPassword, db: DB):
    await auth_service.forgot_password(db, data.email)
    return SuccessResponse(message="Se o email existir, enviámos instruções")


@router.post("/reset-password", response_model=SuccessResponse)
async def reset_password(data: UserPasswordReset, db: DB):
    await auth_service.reset_password(db, data.token, data.new_password)
    return SuccessResponse(message="Palavra-passe alterada")


@router.post("/verify-email", response_model=SuccessResponse)
async def verify_email(token: str, db: DB):
    await auth_service.verify_email(db, token)
    return SuccessResponse(message="Email confirmado")


@router.get("/me", response_model=UserResponse)
async def me(user: CurrentUser):
    return user


@router.put("/me", response_model=UserResponse)
async def update_me(data: UserUpdate, user: CurrentUser, db: DB):
    for k, v in data.model_dump(exclude_unset=True, exclude={"role", "is_active", "institution_id"}).items():
        setattr(user, k, v)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/change-password", response_model=SuccessResponse)
async def change_password(data: UserPasswordChange, user: CurrentUser, db: DB):
    await auth_service.change_password(db, user, data.current_password, data.new_password)
    return SuccessResponse(message="Palavra-passe alterada")
