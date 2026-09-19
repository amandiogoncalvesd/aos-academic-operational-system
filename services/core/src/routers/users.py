from typing import Annotated

from fastapi import APIRouter, Depends, Query, UploadFile, status
from fastapi.responses import PlainTextResponse

from ..dependencies.auth import AdminUser, CurrentUser, require_role
from ..dependencies.database import DB
from ..models import UserRole
from ..schemas import PaginatedResponse, PaginationParams, SuccessResponse, UserCreate, UserResponse, UserUpdate
from ..services import user_service

router = APIRouter(prefix="/users", tags=["Users"])
Staff = require_role(UserRole.admin, UserRole.coordinator, UserRole.secretary, UserRole.hr)


@router.get("", response_model=PaginatedResponse[UserResponse])
async def list_users(db: DB, _: Annotated[object, Staff], params: Annotated[PaginationParams, Depends()],
                     search: str | None = None, role: UserRole | None = None, institution_id: str | None = None):
    return await user_service.get_users(db, params, search, role, institution_id)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: DB, _: AdminUser):
    return await user_service.create_user(db, data)


@router.get("/export", response_class=PlainTextResponse)
async def export_users(db: DB, _: AdminUser):
    return PlainTextResponse(await user_service.export_users(db), media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=users.csv"})


@router.post("/bulk-import")
async def bulk_import(file: UploadFile, db: DB, _: AdminUser):
    return await user_service.bulk_import_users(db, await file.read())


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: DB, me: CurrentUser):
    if me.id != user_id and me.role not in (UserRole.admin, UserRole.coordinator, UserRole.secretary, UserRole.teacher):
        from fastapi import HTTPException
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Sem permissão")
    return await user_service.get_user_by_id(db, user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, data: UserUpdate, db: DB, _: AdminUser):
    return await user_service.update_user(db, user_id, data)


@router.delete("/{user_id}", response_model=SuccessResponse)
async def delete_user(user_id: str, db: DB, _: AdminUser):
    await user_service.delete_user(db, user_id)
    return SuccessResponse(message="Utilizador removido")
