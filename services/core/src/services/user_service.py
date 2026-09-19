import csv
import io

from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User, UserRole
from ..plugins import event_bus
from ..schemas.common import PaginationParams
from ..schemas.user import UserCreate, UserUpdate
from ..utils.pagination import paginate
from ..utils.security import hash_password


async def get_users(db: AsyncSession, params: PaginationParams, search: str | None = None,
                    role: UserRole | None = None, institution_id: str | None = None):
    q = select(User).order_by(User.created_at.desc())
    if search:
        like = f"%{search}%"
        q = q.where(or_(User.email.ilike(like), User.first_name.ilike(like), User.last_name.ilike(like)))
    if role:
        q = q.where(User.role == role)
    if institution_id:
        q = q.where(User.institution_id == institution_id)
    return await paginate(db, q, params)


async def get_user_by_id(db: AsyncSession, user_id: str) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Utilizador não encontrado")
    return user


async def create_user(db: AsyncSession, data: UserCreate) -> User:
    user = User(**data.model_dump(exclude={"password"}), password_hash=hash_password(data.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    await event_bus.publish("auth.user.created", {"user_id": user.id, "role": user.role.value})
    return user


async def update_user(db: AsyncSession, user_id: str, data: UserUpdate) -> User:
    user = await get_user_by_id(db, user_id)
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(user, k, v)
    await db.commit()
    await db.refresh(user)
    await event_bus.publish("auth.user.updated", {"user_id": user.id})
    return user


async def delete_user(db: AsyncSession, user_id: str) -> None:
    user = await get_user_by_id(db, user_id)
    await db.delete(user)
    await db.commit()
    await event_bus.publish("auth.user.deleted", {"user_id": user_id})


async def bulk_import_users(db: AsyncSession, content: bytes, default_password: str = "Mudar123!") -> dict:
    reader = csv.DictReader(io.StringIO(content.decode("utf-8-sig")))
    created, errors = 0, []
    for i, row in enumerate(reader, start=2):
        try:
            data = UserCreate(email=row["email"], first_name=row["first_name"], last_name=row["last_name"],
                              role=row.get("role") or "student", password=row.get("password") or default_password)
            db.add(User(**data.model_dump(exclude={"password"}), password_hash=hash_password(data.password)))
            created += 1
        except Exception as exc:
            errors.append({"line": i, "error": str(exc)})
    await db.commit()
    return {"created": created, "errors": errors}


async def export_users(db: AsyncSession) -> str:
    users = (await db.execute(select(User))).scalars().all()
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["id", "email", "first_name", "last_name", "role", "is_active", "created_at"])
    for u in users:
        w.writerow([u.id, u.email, u.first_name, u.last_name, u.role.value, u.is_active, u.created_at])
    return buf.getvalue()
