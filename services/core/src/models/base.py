import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class BaseModel(Base, TimestampMixin):
    """Base abstrata: id UUID (string p/ portabilidade Postgres/SQLite) + timestamps."""

    __abstract__ = True
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
