from fastapi import APIRouter

from ..dependencies.auth import AdminUser, CurrentUser
from ..dependencies.database import DB
from ..schemas import SettingBulkUpdate, SettingResponse, SettingUpsert, SuccessResponse
from ..services import setting_service as svc

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("", response_model=list[SettingResponse])
async def list_settings(db: DB, _: CurrentUser, institution_id: str | None = None, plugin_id: str | None = None):
    return await svc.get_settings(db, institution_id, plugin_id)


@router.post("/bulk-update", response_model=list[SettingResponse])
async def bulk_update(data: SettingBulkUpdate, db: DB, _: AdminUser):
    return await svc.bulk_update_settings(db, data.settings, data.institution_id)


@router.get("/{key}", response_model=SettingResponse)
async def get_setting(key: str, db: DB, _: CurrentUser, institution_id: str | None = None, plugin_id: str | None = None):
    return await svc.get_setting(db, key, institution_id, plugin_id)


@router.put("/{key}", response_model=SettingResponse)
async def put_setting(key: str, data: SettingUpsert, db: DB, _: AdminUser):
    return await svc.set_setting(db, key, data.value, data.type, data.institution_id, data.plugin_id)


@router.delete("/{key}", response_model=SuccessResponse)
async def delete_setting(key: str, db: DB, _: AdminUser, institution_id: str | None = None, plugin_id: str | None = None):
    await svc.delete_setting(db, key, institution_id, plugin_id)
    return SuccessResponse()
