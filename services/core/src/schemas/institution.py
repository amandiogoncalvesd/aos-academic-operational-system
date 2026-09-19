from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..models.institution import InstitutionPlan


class InstitutionBase(BaseModel):
    name: str = Field(max_length=200)
    slug: str = Field(pattern=r"^[a-z0-9-]+$", max_length=100)
    logo_url: str | None = None
    primary_color: str = "#3363ff"
    secondary_color: str = "#19288f"
    domain: str | None = None
    plan: InstitutionPlan = InstitutionPlan.free


class InstitutionCreate(InstitutionBase):
    settings: dict = {}


class InstitutionUpdate(BaseModel):
    name: str | None = None
    logo_url: str | None = None
    primary_color: str | None = None
    secondary_color: str | None = None
    domain: str | None = None
    plan: InstitutionPlan | None = None
    is_active: bool | None = None
    settings: dict | None = None


class InstitutionResponse(InstitutionBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    settings: dict
    is_active: bool
    created_at: datetime
