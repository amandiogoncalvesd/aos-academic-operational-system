import uuid
from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="-")


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        cid = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        correlation_id.set(cid)
        request.state.correlation_id = cid
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = cid
        return response
