"""Regista automaticamente mutações (POST/PUT/PATCH/DELETE) autenticadas em audit_logs."""
import logging

from starlette.middleware.base import BaseHTTPMiddleware

from ..database import AsyncSessionLocal
from ..models import AuditLog

log = logging.getLogger("aos.audit")
MUTATING = {"POST", "PUT", "PATCH", "DELETE"}
SKIP_PREFIXES = ("/api/v1/auth/login", "/api/v1/auth/refresh", "/health", "/docs")


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.method in MUTATING and not request.url.path.startswith(SKIP_PREFIXES) and response.status_code < 400:
            user_id = getattr(request.state, "user_id", None)
            parts = [p for p in request.url.path.split("/") if p]
            resource = parts[2] if len(parts) > 2 else (parts[-1] if parts else "-")
            resource_id = parts[3] if len(parts) > 3 else None
            try:
                async with AsyncSessionLocal() as db:
                    db.add(AuditLog(user_id=user_id, action=request.method.lower(), resource=resource,
                                    resource_id=resource_id, ip_address=request.client.host if request.client else None,
                                    user_agent=request.headers.get("user-agent", "")[:500],
                                    new_values={"path": request.url.path, "status": response.status_code}))
                    await db.commit()
            except Exception:
                log.exception("falha ao gravar audit log")
        return response
