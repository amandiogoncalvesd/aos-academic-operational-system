from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Setting
from ..plugins import event_bus


def _scope(q, institution_id: str | None, plugin_id: str | None):
    return q.where(Setting.institution_id.is_(institution_id) if institution_id is None else Setting.institution_id == institution_id,
                   Setting.plugin_id.is_(plugin_id) if plugin_id is None else Setting.plugin_id == plugin_id)


async def get_settings(db: AsyncSession, institution_id: str | None = None, plugin_id: str | None = None) -> list[Setting]:
    return list((await db.execute(_scope(select(Setting), institution_id, plugin_id).order_by(Setting.key))).scalars().all())


async def get_setting(db: AsyncSession, key: str, institution_id=None, plugin_id=None) -> Setting:
    s = (await db.execute(_scope(select(Setting).where(Setting.key == key), institution_id, plugin_id))).scalar_one_or_none()
    if not s:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Setting '{key}' não encontrado")
    return s


async def set_setting(db: AsyncSession, key: str, value: Any, type_: str = "string",
                      institution_id=None, plugin_id=None) -> Setting:
    s = (await db.execute(_scope(select(Setting).where(Setting.key == key), institution_id, plugin_id))).scalar_one_or_none()
    if s:
        s.value, s.type = value, type_
    else:
        s = Setting(key=key, value=value, type=type_, institution_id=institution_id, plugin_id=plugin_id)
        db.add(s)
    await db.commit()
    await db.refresh(s)
    await event_bus.publish("config.setting.changed", {"key": key, "institution_id": institution_id})
    return s


async def delete_setting(db: AsyncSession, key: str, institution_id=None, plugin_id=None) -> None:
    await db.delete(await get_setting(db, key, institution_id, plugin_id))
    await db.commit()


async def bulk_update_settings(db: AsyncSession, values: dict[str, Any], institution_id=None) -> list[Setting]:
    return [await set_setting(db, k, v, "json" if isinstance(v, (dict, list)) else type(v).__name__, institution_id)
            for k, v in values.items()]
