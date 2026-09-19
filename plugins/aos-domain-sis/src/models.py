from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel


class Course(BaseModel):
    __tablename__ = "sis_courses"

    code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(String(2000))
    credits: Mapped[int] = mapped_column(Integer, default=0)
    capacity: Mapped[int] = mapped_column(Integer, default=30)
    teacher_id: Mapped[str | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    institution_id: Mapped[str | None] = mapped_column(ForeignKey("institutions.id", ondelete="CASCADE"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Enrollment(BaseModel):
    __tablename__ = "sis_enrollments"
    __table_args__ = (UniqueConstraint("course_id", "student_id", "term", name="uq_enrollment"),)

    course_id: Mapped[str] = mapped_column(ForeignKey("sis_courses.id", ondelete="CASCADE"), index=True)
    student_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    term: Mapped[str] = mapped_column(String(20), default="2026/2027")
    status: Mapped[str] = mapped_column(String(20), default="active")  # active | cancelled | completed
