import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware

log = logging.getLogger("aos.http")


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        ms = (time.perf_counter() - start) * 1000
        response.headers["X-Response-Time"] = f"{ms:.1f}ms"
        log.info("%s %s -> %s %.1fms", request.method, request.url.path, response.status_code, ms)
        return response
