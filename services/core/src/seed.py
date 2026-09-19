"""Dados iniciais: instituição G Designer School, papéis de sistema e admin."""
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Institution, Role, User, UserRole
from .utils.security import hash_password

log = logging.getLogger("aos.seed")

SYSTEM_ROLES = {
    "admin": ["*"],
    "coordinator": ["sis.*", "lms.*", "users.read", "reports.*"],
    "teacher": ["lms.course.read", "lms.content.manage", "lms.grade.manage", "sis.attendance.manage"],
    "student": ["lms.course.read", "lms.assignment.submit", "sis.grades.read.own"],
    "secretary": ["sis.*", "users.read", "erp.invoice.read"],
    "librarian": ["library.*"],
    "hr": ["hr.*", "users.read"],
    "parent": ["sis.grades.read.child", "erp.invoice.read.child"],
    "guest": [],
}


async def seed_defaults(db: AsyncSession) -> None:
    inst = (await db.execute(select(Institution).where(Institution.slug == "g-designer-school"))).scalar_one_or_none()
    if not inst:
        inst = Institution(name="G Designer School", slug="g-designer-school", domain="gdesigner.school",
                           primary_color="#1f4bd8", secondary_color="#0f1f4d", plan="pro",
                           settings={"locale": "pt-AO", "timezone": "Africa/Luanda", "currency": "AOA",
                                     "academic_year": "2026/2027", "min_grade": 10, "min_attendance": 75})
        db.add(inst)
        await db.flush()
        log.info("instituição criada: %s", inst.name)

    for name, perms in SYSTEM_ROLES.items():
        if not (await db.execute(select(Role).where(Role.name == name, Role.is_system_role.is_(True)))).scalar_one_or_none():
            db.add(Role(name=name, permissions=perms, is_system_role=True))

    if not (await db.execute(select(User).where(User.email == "admin@gdesigner.school"))).scalar_one_or_none():
        db.add(User(email="admin@gdesigner.school", password_hash=hash_password("Admin123!"),
                    first_name="Admin", last_name="AOS", role=UserRole.admin, is_verified=True, institution_id=inst.id))
        log.info("admin criado: admin@gdesigner.school / Admin123!")
    await db.commit()
