from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select

from ..dependencies.auth import AdminUser, CurrentUser
from ..dependencies.database import DB
from ..models import Role
from ..schemas import SuccessResponse

router = APIRouter(prefix="/roles", tags=["Roles"])


class RoleIn(BaseModel):
    name: str
    permissions: list[str] = []
    institution_id: str | None = None


class RoleOut(RoleIn):
    model_config = ConfigDict(from_attributes=True)
    id: str
    is_system_role: bool


async def _get(db, role_id):
    r = await db.get(Role, role_id)
    if not r:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Papel não encontrado")
    return r


@router.get("", response_model=list[RoleOut])
async def list_roles(db: DB, _: CurrentUser):
    return list((await db.execute(select(Role).order_by(Role.name))).scalars().all())


@router.post("", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
async def create_role(data: RoleIn, db: DB, _: AdminUser):
    r = Role(**data.model_dump())
    db.add(r)
    await db.commit()
    await db.refresh(r)
    return r


@router.get("/{role_id}", response_model=RoleOut)
async def get_role(role_id: str, db: DB, _: CurrentUser):
    return await _get(db, role_id)


@router.put("/{role_id}", response_model=RoleOut)
async def update_role(role_id: str, data: RoleIn, db: DB, _: AdminUser):
    r = await _get(db, role_id)
    for k, v in data.model_dump().items():
        setattr(r, k, v)
    await db.commit()
    await db.refresh(r)
    return r


@router.delete("/{role_id}", response_model=SuccessResponse)
async def delete_role(role_id: str, db: DB, _: AdminUser):
    r = await _get(db, role_id)
    if r.is_system_role:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Papel de sistema")
    await db.delete(r)
    await db.commit()
    return SuccessResponse()


@router.get("/{role_id}/permissions", response_model=list[str])
async def role_permissions(role_id: str, db: DB, _: CurrentUser):
    return (await _get(db, role_id)).permissions
