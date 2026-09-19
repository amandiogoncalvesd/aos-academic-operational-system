from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogCreate(BaseModel):
    user_id: str | None = None
    action: str
    resource: str
    resource_id: str | None = None
    old_values: dict | None = None
    new_values: dict | None = None
    ip_address: str | None = None
    user_agent: str | None = None


class AuditLogResponse(AuditLogCreate):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime


class AuditLogFilter(BaseModel):
    user_id: str | None = None
    action: str | None = None
    resource: str | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
