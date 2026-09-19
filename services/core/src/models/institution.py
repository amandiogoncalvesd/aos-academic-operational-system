import enum

from sqlalchemy import JSON, Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class InstitutionPlan(str, enum.Enum):
    free = "free"
    basic = "basic"
    pro = "pro"
    enterprise = "enterprise"


class Institution(BaseModel):
    __tablename__ = "institutions"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(String(500))
    primary_color: Mapped[str] = mapped_column(String(9), default="#3363ff")
    secondary_color: Mapped[str] = mapped_column(String(9), default="#19288f")
    domain: Mapped[str | None] = mapped_column(String(255), unique=True)
    settings: Mapped[dict] = mapped_column(JSON, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    plan: Mapped[InstitutionPlan] = mapped_column(Enum(InstitutionPlan), default=InstitutionPlan.free)

    users = relationship("User", back_populates="institution")
