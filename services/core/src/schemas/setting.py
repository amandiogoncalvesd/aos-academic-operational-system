from typing import Any

from pydantic import BaseModel, ConfigDict


class SettingUpsert(BaseModel):
    value: Any
    type: str = "string"
    institution_id: str | None = None
    plugin_id: str | None = None


class SettingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    key: str
    value: Any
    type: str
    institution_id: str | None
    plugin_id: str | None


class SettingBulkUpdate(BaseModel):
    settings: dict[str, Any]
    institution_id: str | None = None
