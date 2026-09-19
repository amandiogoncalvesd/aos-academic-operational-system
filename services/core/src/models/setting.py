from sqlalchemy import JSON, Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Setting(BaseModel):
    __tablename__ = "settings"
    __table_args__ = (UniqueConstraint("key", "institution_id", "plugin_id", name="uq_setting_scope"),)

    key: Mapped[str] = mapped_column(String(150), index=True)
    value: Mapped[dict | list | str | int | float | bool | None] = mapped_column(JSON)
    type: Mapped[str] = mapped_column(String(20), default="string")  # string|int|float|bool|json
    institution_id: Mapped[str | None] = mapped_column(ForeignKey("institutions.id", ondelete="CASCADE"))
    plugin_id: Mapped[str | None] = mapped_column(ForeignKey("plugins.id", ondelete="CASCADE"))
    is_encrypted: Mapped[bool] = mapped_column(Boolean, default=False)
