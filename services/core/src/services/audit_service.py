import csv
import io

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import AuditLog
from ..schemas.audit_log import AuditLogCreate, AuditLogFilter
from ..schemas.common import PaginationParams
from ..utils.pagination import paginate


async def log_action(db: AsyncSession, data: AuditLogCreate) -> AuditLog:
    entry = AuditLog(**data.model_dump())
    db.add(entry)
    await db.commit()
    return entry


def _apply(q, f: AuditLogFilter):
    if f.user_id:
        q = q.where(AuditLog.user_id == f.user_id)
    if f.action:
        q = q.where(AuditLog.action == f.action)
    if f.resource:
        q = q.where(AuditLog.resource == f.resource)
    if f.date_from:
        q = q.where(AuditLog.created_at >= f.date_from)
    if f.date_to:
        q = q.where(AuditLog.created_at <= f.date_to)
    return q


async def get_audit_logs(db: AsyncSession, f: AuditLogFilter, params: PaginationParams):
    return await paginate(db, _apply(select(AuditLog).order_by(AuditLog.created_at.desc()), f), params)


async def export_audit_logs(db: AsyncSession, f: AuditLogFilter) -> str:
    rows = (await db.execute(_apply(select(AuditLog), f))).scalars().all()
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["id", "created_at", "user_id", "action", "resource", "resource_id", "ip_address"])
    for r in rows:
        w.writerow([r.id, r.created_at, r.user_id, r.action, r.resource, r.resource_id, r.ip_address])
    return buf.getvalue()
