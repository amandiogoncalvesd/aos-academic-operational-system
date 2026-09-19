from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NotificationCreate(BaseModel):
    user_id: str
    type: str = "info"
    title: str
    message: str
    data: dict | None = None


class NotificationUpdate(BaseModel):
    is_read: bool


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    type: str
    title: str
    message: str
    data: dict | None
    is_read: bool
    read_at: datetime | None
    created_at: datetime
