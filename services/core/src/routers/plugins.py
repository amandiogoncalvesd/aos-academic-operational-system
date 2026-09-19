from fastapi import APIRouter

from ..dependencies.auth import AdminUser, CurrentUser
from ..dependencies.database import DB
from ..plugins import plugin_engine
from ..schemas import PluginConfigUpdate, PluginInstall, PluginResponse, SuccessResponse
from ..services import plugin_service as svc

router = APIRouter(prefix="/plugins", tags=["Plugins"])


@router.get("", response_model=list[PluginResponse])
async def list_plugins(db: DB, _: CurrentUser):
    await svc.sync_plugins(db)
    return await svc.get_plugins(db)


@router.get("/registry")
async def registry(_: CurrentUser):
    """Estado em memória do Plugin Engine: hooks, eventos, navegação."""
    return {**plugin_engine.describe(), "nav": plugin_engine.nav,
            "manifests": {k: v.manifest.to_public() for k, v in plugin_engine.plugins.items()}}


@router.post("/install", response_model=PluginResponse)
async def install(data: PluginInstall, db: DB, _: AdminUser):
    return await svc.install_plugin(db, data.slug)


@router.post("/{plugin_id}/activate", response_model=PluginResponse)
async def activate(plugin_id: str, db: DB, _: AdminUser):
    return await svc.activate_plugin(db, plugin_id)


@router.post("/{plugin_id}/deactivate", response_model=PluginResponse)
async def deactivate(plugin_id: str, db: DB, _: AdminUser):
    return await svc.deactivate_plugin(db, plugin_id)


@router.delete("/{plugin_id}", response_model=SuccessResponse)
async def uninstall(plugin_id: str, db: DB, _: AdminUser):
    await svc.uninstall_plugin(db, plugin_id)
    return SuccessResponse()


@router.get("/{plugin_id}/config")
async def get_config(plugin_id: str, db: DB, _: AdminUser):
    return await svc.get_plugin_config(db, plugin_id)


@router.put("/{plugin_id}/config")
async def put_config(plugin_id: str, data: PluginConfigUpdate, db: DB, _: AdminUser):
    return await svc.update_plugin_config(db, plugin_id, data.config)
