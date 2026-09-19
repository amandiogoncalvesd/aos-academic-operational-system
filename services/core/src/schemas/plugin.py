from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PluginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    slug: str
    version: str
    description: str | None
    author: str | None
    is_active: bool
    is_system: bool
    config: dict
    permissions: list
    created_at: datetime


class PluginInstall(BaseModel):
    slug: str


class PluginConfigUpdate(BaseModel):
    config: dict
