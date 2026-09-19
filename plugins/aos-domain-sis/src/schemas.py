from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
    code: str = Field(max_length=20)
    name: str
    description: str | None = None
    credits: int = 0
    capacity: int = 30
    teacher_id: str | None = None
    institution_id: str | None = None


class CourseOut(CourseCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str
    is_active: bool
    created_at: datetime


class EnrollmentCreate(BaseModel):
    course_id: str
    student_id: str | None = None  # None → o próprio utilizador
    term: str = "2026/2027"


class EnrollmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    course_id: str
    student_id: str
    term: str
    status: str
    created_at: datetime
