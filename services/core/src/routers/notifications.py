from typing import Annotated

from fastapi import APIRouter, Depends

from ..dependencies.auth import CurrentUser
from ..dependencies.database import DB
from ..schemas import NotificationResponse, PaginatedResponse, PaginationParams, SuccessResponse
from ..services import notification_service as svc

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=PaginatedResponse[NotificationResponse])
async def list_notifications(db: DB, user: CurrentUser, params: Annotated[PaginationParams, Depends()],
                             unread_only: bool = False):
    return await svc.get_user_notifications(db, user.id, params, unread_only)


@router.get("/unread-count")
async def unread_count(db: DB, user: CurrentUser):
    return {"count": await svc.unread_count(db, user.id)}


@router.post("/read-all", response_model=SuccessResponse)
async def read_all(db: DB, user: CurrentUser):
    await svc.mark_all_as_read(db, user.id)
    return SuccessResponse()


@router.post("/{notification_id}/read", response_model=NotificationResponse)
async def read_one(notification_id: str, db: DB, user: CurrentUser):
    return await svc.mark_as_read(db, user.id, notification_id)


@router.delete("/{notification_id}", response_model=SuccessResponse)
async def delete_one(notification_id: str, db: DB, user: CurrentUser):
    await svc.delete_notification(db, user.id, notification_id)
    return SuccessResponse()
