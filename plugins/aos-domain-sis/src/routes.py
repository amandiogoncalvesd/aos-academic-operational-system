from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from src.dependencies.auth import CurrentUser, require_role
from src.dependencies.database import DB
from src.models import User, UserRole
from src.plugins import event_bus, plugin_engine

from .models import Course, Enrollment
from .schemas import CourseCreate, CourseOut, EnrollmentCreate, EnrollmentOut

router = APIRouter()
Staff = require_role(UserRole.admin, UserRole.coordinator, UserRole.secretary)


@router.get("/courses", response_model=list[CourseOut])
async def list_courses(db: DB, _: CurrentUser):
    return list((await db.execute(select(Course).where(Course.is_active.is_(True)).order_by(Course.code))).scalars().all())


@router.post("/courses", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
async def create_course(data: CourseCreate, db: DB, user: CurrentUser):
    if user.role not in (UserRole.admin, UserRole.coordinator):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Apenas coordenação pode criar cursos")
    if (await db.execute(select(Course).where(Course.code == data.code))).scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, "Código de curso já existe")
    course = Course(**{**data.model_dump(), "institution_id": data.institution_id or user.institution_id})
    db.add(course)
    await db.commit()
    await db.refresh(course)
    await event_bus.publish("sis.course.created", {"course_id": course.id, "code": course.code, "name": course.name})
    return course


@router.get("/courses/{course_id}", response_model=CourseOut)
async def get_course(course_id: str, db: DB, _: CurrentUser):
    c = await db.get(Course, course_id)
    if not c:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Curso não encontrado")
    return c


@router.get("/enrollments", response_model=list[EnrollmentOut])
async def list_enrollments(db: DB, user: CurrentUser, course_id: str | None = None):
    q = select(Enrollment)
    if user.role == UserRole.student:
        q = q.where(Enrollment.student_id == user.id)
    if course_id:
        q = q.where(Enrollment.course_id == course_id)
    return list((await db.execute(q.order_by(Enrollment.created_at.desc()))).scalars().all())


@router.post("/enrollments", response_model=EnrollmentOut, status_code=status.HTTP_201_CREATED)
async def enroll(data: EnrollmentCreate, db: DB, user: CurrentUser):
    student_id = data.student_id or user.id
    if student_id != user.id and user.role not in (UserRole.admin, UserRole.coordinator, UserRole.secretary):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Sem permissão para matricular terceiros")
    course = await db.get(Course, data.course_id)
    if not course:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Curso não encontrado")
    taken = (await db.execute(select(func.count()).select_from(Enrollment)
                              .where(Enrollment.course_id == course.id, Enrollment.status == "active"))).scalar_one()
    # Filter hook: outros plugins (ERP: propinas em dívida; pré-requisitos) podem vetar
    verdict = await plugin_engine.apply_filters("sis.enrollment.validate",
                                                {"ok": taken < course.capacity, "reason": "Turma lotada"},
                                                course=course, student_id=student_id)
    if not verdict["ok"]:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, verdict["reason"])
    if (await db.execute(select(Enrollment).where(Enrollment.course_id == course.id, Enrollment.student_id == student_id,
                                                  Enrollment.term == data.term))).scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, "Já matriculado")
    enr = Enrollment(course_id=course.id, student_id=student_id, term=data.term)
    db.add(enr)
    await db.commit()
    await db.refresh(enr)
    student = await db.get(User, student_id)
    await event_bus.publish("sis.student.enrolled", {
        "enrollment_id": enr.id, "user_id": student_id, "student_email": student.email if student else None,
        "course_id": course.id, "course_code": course.code, "course_name": course.name, "term": enr.term,
    })
    await plugin_engine.do_action("sis.enrollment.after_create", enr)
    return enr


@router.delete("/enrollments/{enrollment_id}", response_model=EnrollmentOut)
async def cancel(enrollment_id: str, db: DB, user: CurrentUser):
    enr = await db.get(Enrollment, enrollment_id)
    if not enr:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Matrícula não encontrada")
    if enr.student_id != user.id and user.role not in (UserRole.admin, UserRole.coordinator, UserRole.secretary):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Sem permissão")
    enr.status = "cancelled"
    await db.commit()
    await event_bus.publish("sis.enrollment.cancelled", {"enrollment_id": enr.id, "user_id": enr.student_id})
    return enr
