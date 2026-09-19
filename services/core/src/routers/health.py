from fastapi import APIRouter
from sqlalchemy import text

from ..config import settings
from ..database import engine
from ..plugins import plugin_engine

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT, "event_bus": settings.EVENT_BUS_BACKEND,
            "plugins": {k: v.status for k, v in plugin_engine.plugins.items()}}


@router.get("/db")
async def health_db():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "driver": engine.dialect.name}
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}


@router.get("/redis")
async def health_redis():
    try:
        import redis.asyncio as aioredis
        r = aioredis.from_url(settings.REDIS_URL)
        pong = await r.ping()
        await r.aclose()
        return {"status": "ok" if pong else "error"}
    except Exception as exc:
        return {"status": "unavailable", "detail": str(exc)}


@router.get("/kafka")
async def health_kafka():
    if settings.EVENT_BUS_BACKEND != "kafka":
        return {"status": "disabled", "detail": f"event bus backend = {settings.EVENT_BUS_BACKEND}"}
    try:
        from aiokafka import AIOKafkaProducer
        p = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
        await p.start()
        await p.stop()
        return {"status": "ok"}
    except Exception as exc:
        return {"status": "unavailable", "detail": str(exc)}
