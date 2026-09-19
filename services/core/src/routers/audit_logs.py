from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse

from ..dependencies.auth import AdminUser
from ..dependencies.database import DB
from ..schemas import AuditLogFilter, AuditLogResponse, PaginatedResponse, PaginationParams
from ..services import audit_service

router = APIRouter(prefix="/audit-logs", tags=["Audit"])


@router.get("", response_model=PaginatedResponse[AuditLogResponse])
async def list_logs(db: DB, _: AdminUser, params: Annotated[PaginationParams, Depends()],
                    f: Annotated[AuditLogFilter, Depends()]):
    return await audit_service.get_audit_logs(db, f, params)


@router.get("/export", response_class=PlainTextResponse)
async def export_logs(db: DB, _: AdminUser, f: Annotated[AuditLogFilter, Depends()]):
    return PlainTextResponse(await audit_service.export_audit_logs(db, f), media_type="text/csv")


@router.get("/{log_id}", response_model=AuditLogResponse)
async def get_log(log_id: str, db: DB, _: AdminUser):
    from ..models import AuditLog
    entry = await db.get(AuditLog, log_id)
    if not entry:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Registo não encontrado")
    return entry
