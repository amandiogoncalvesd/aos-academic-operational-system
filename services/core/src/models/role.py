from sqlalchemy import JSON, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    permissions: Mapped[list] = mapped_column(JSON, default=list)  # ["lms.course.create", ...]
    institution_id: Mapped[str | None] = mapped_column(ForeignKey("institutions.id", ondelete="CASCADE"))
    is_system_role: Mapped[bool] = mapped_column(Boolean, default=False)
