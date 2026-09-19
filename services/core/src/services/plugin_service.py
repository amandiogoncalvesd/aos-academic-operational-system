"""Sincroniza plugins descobertos em disco com a tabela `plugins` e expõe operações."""
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Plugin
from ..plugins import event_bus, plugin_engine


async def sync_plugins(db: AsyncSession) -> None:
    for pid, loaded in plugin_engine.plugins.items():
        m = loaded.manifest
        row = (await db.execute(select(Plugin).where(Plugin.slug == pid))).scalar_one_or_none()
        if not row:
            row = Plugin(slug=pid, name=m.name, is_system=(m.type == "core"), is_active=(loaded.status == "active"))
            db.add(row)
        row.version, row.description, row.author, row.permissions = m.version, m.description, m.author, m.permissions
    await db.commit()


async def get_plugins(db: AsyncSession) -> list[Plugin]:
    return list((await db.execute(select(Plugin).order_by(Plugin.name))).scalars().all())


async def _get(db: AsyncSession, plugin_id: str) -> Plugin:
    p = await db.get(Plugin, plugin_id) or (await db.execute(select(Plugin).where(Plugin.slug == plugin_id))).scalar_one_or_none()
    if not p:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Plugin não encontrado")
    return p


async def install_plugin(db: AsyncSession, slug: str) -> Plugin:
    if slug not in plugin_engine.plugins:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Plugin '{slug}' não existe em plugins/")
    await sync_plugins(db)
    return await _get(db, slug)


async def activate_plugin(db: AsyncSession, plugin_id: str) -> Plugin:
    p = await _get(db, plugin_id)
    p.is_active = True
    await db.commit()
    await event_bus.publish("core.plugin.activated", {"plugin": p.slug})
    return p


async def deactivate_plugin(db: AsyncSession, plugin_id: str) -> Plugin:
    p = await _get(db, plugin_id)
    if p.is_system:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Plugins de sistema não podem ser desactivados")
    p.is_active = False
    plugin_engine.remove_plugin_hooks(p.slug)
    await db.commit()
    await event_bus.publish("core.plugin.deactivated", {"plugin": p.slug})
    return p


async def uninstall_plugin(db: AsyncSession, plugin_id: str) -> None:
    p = await _get(db, plugin_id)
    if p.is_system:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Plugins de sistema não podem ser removidos")
    plugin_engine.remove_plugin_hooks(p.slug)
    await db.delete(p)
    await db.commit()


async def get_plugin_config(db: AsyncSession, plugin_id: str) -> dict:
    return (await _get(db, plugin_id)).config


async def update_plugin_config(db: AsyncSession, plugin_id: str, config: dict) -> dict:
    p = await _get(db, plugin_id)
    p.config = {**(p.config or {}), **config}
    await db.commit()
    await event_bus.publish("core.plugin.config_updated", {"plugin": p.slug, "config": p.config})
    return p.config
