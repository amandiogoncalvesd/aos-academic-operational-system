from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from ..dependencies.auth import AdminUser, CurrentUser
from ..dependencies.database import DB
from ..models import Institution
from ..plugins import event_bus
from ..schemas import InstitutionCreate, InstitutionResponse, InstitutionUpdate, SuccessResponse

router = APIRouter(prefix="/institutions", tags=["Institutions"])


async def _get(db, inst_id: str) -> Institution:
    inst = await db.get(Institution, inst_id)
    if not inst:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Instituição não encontrada")
    return inst


@router.get("", response_model=list[InstitutionResponse])
async def list_institutions(db: DB, _: CurrentUser):
    return list((await db.execute(select(Institution).order_by(Institution.name))).scalars().all())


@router.post("", response_model=InstitutionResponse, status_code=status.HTTP_201_CREATED)
async def create_institution(data: InstitutionCreate, db: DB, _: AdminUser):
    if (await db.execute(select(Institution).where(Institution.slug == data.slug))).scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, "Slug já existe")
    inst = Institution(**data.model_dump())
    db.add(inst)
    await db.commit()
    await db.refresh(inst)
    await event_bus.publish("core.institution.created", {"institution_id": inst.id, "slug": inst.slug})
    return inst


@router.get("/{inst_id}", response_model=InstitutionResponse)
async def get_institution(inst_id: str, db: DB, _: CurrentUser):
    return await _get(db, inst_id)


@router.put("/{inst_id}", response_model=InstitutionResponse)
async def update_institution(inst_id: str, data: InstitutionUpdate, db: DB, _: AdminUser):
    inst = await _get(db, inst_id)
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(inst, k, v)
    await db.commit()
    await db.refresh(inst)
    return inst


@router.delete("/{inst_id}", response_model=SuccessResponse)
async def delete_institution(inst_id: str, db: DB, _: AdminUser):
    await db.delete(await _get(db, inst_id))
    await db.commit()
    return SuccessResponse(message="Instituição removida")


@router.get("/{inst_id}/settings")
async def get_institution_settings(inst_id: str, db: DB, _: CurrentUser):
    return (await _get(db, inst_id)).settings


@router.put("/{inst_id}/settings")
async def update_institution_settings(inst_id: str, data: dict, db: DB, _: AdminUser):
    inst = await _get(db, inst_id)
    inst.settings = {**(inst.settings or {}), **data}
    await db.commit()
    return inst.settings
