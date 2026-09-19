"""AOS Core — ponto de entrada FastAPI."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from .config import settings
from .database import AsyncSessionLocal, init_db
from .dependencies.rate_limit import limiter
from .middleware.audit import AuditMiddleware
from .middleware.correlation import CorrelationIdMiddleware
from .middleware.timing import TimingMiddleware
from .plugins import event_bus, load_plugins, plugin_engine
from .routers import include_routers

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("aos")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await event_bus.start()
    await init_db()
    async with AsyncSessionLocal() as db:
        from .services.plugin_service import sync_plugins
        from .seed import seed_defaults
        await seed_defaults(db)
        await sync_plugins(db)
    await plugin_engine.do_action("core.ready", app)
    await event_bus.publish("core.started", {"version": settings.APP_VERSION,
                                             "plugins": list(plugin_engine.plugins)})
    log.info("AOS Core %s pronto — %d plugins", settings.APP_VERSION, len(plugin_engine.plugins))
    yield
    await event_bus.stop()


app = FastAPI(
    title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=lifespan,
    description="Núcleo do Academic Operational System: auth, utilizadores, instituições, plugins, event bus.",
    docs_url="/docs", redoc_url="/redoc", openapi_url=f"{settings.API_PREFIX}/openapi.json",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(AuditMiddleware)
app.add_middleware(TimingMiddleware)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_origin_regex=r"https://.*\.e2b\.app",
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status.HTTP_422_UNPROCESSABLE_ENTITY, {
        "detail": "Dados inválidos", "code": "validation_error", "errors": exc.errors(),
        "correlation_id": getattr(request.state, "correlation_id", None)})


@app.exception_handler(Exception)
async def unhandled_handler(request: Request, exc: Exception):
    log.exception("erro não tratado")
    return JSONResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, {
        "detail": "Erro interno", "code": "internal_error",
        "correlation_id": getattr(request.state, "correlation_id", None)})


# Plugins são carregados na importação para que as rotas entrem no OpenAPI
include_routers(app)
load_plugins(app)


@app.get("/", include_in_schema=False)
async def root():
    return {"name": settings.APP_NAME, "docs": "/docs", "health": "/health", "api": settings.API_PREFIX}
