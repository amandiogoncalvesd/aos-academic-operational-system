from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Notification
from ..plugins import event_bus
from ..schemas.common import PaginationParams
from ..schemas.notification import NotificationCreate
from ..utils.pagination import paginate


async def create_notification(db: AsyncSession, data: NotificationCreate) -> Notification:
    n = Notification(**data.model_dump())
    db.add(n)
    await db.commit()
    await db.refresh(n)
    await event_bus.publish("notify.notification.created", {"notification_id": n.id, "user_id": n.user_id})
    return n


async def get_user_notifications(db: AsyncSession, user_id: str, params: PaginationParams, unread_only=False):
    q = select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc())
    if unread_only:
        q = q.where(Notification.is_read.is_(False))
    return await paginate(db, q, params)


async def unread_count(db: AsyncSession, user_id: str) -> int:
    return (await db.execute(select(func.count()).select_from(Notification)
                             .where(Notification.user_id == user_id, Notification.is_read.is_(False)))).scalar_one()


async def mark_as_read(db: AsyncSession, user_id: str, notification_id: str) -> Notification:
    n = await db.get(Notification, notification_id)
    if not n or n.user_id != user_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Notificação não encontrada")
    n.is_read, n.read_at = True, datetime.now(timezone.utc)
    await db.commit()
    return n


async def mark_all_as_read(db: AsyncSession, user_id: str) -> None:
    await db.execute(update(Notification).where(Notification.user_id == user_id, Notification.is_read.is_(False))
                     .values(is_read=True, read_at=datetime.now(timezone.utc)))
    await db.commit()


async def delete_notification(db: AsyncSession, user_id: str, notification_id: str) -> None:
    n = await db.get(Notification, notification_id)
    if not n or n.user_id != user_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Notificação não encontrada")
    await db.delete(n)
    await db.commit()
