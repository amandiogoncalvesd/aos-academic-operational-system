"""Introspecção do Event Bus (dev) + SSE em tempo real para o frontend."""
import asyncio
import json

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from ..dependencies.auth import AdminUser, CurrentUser
from ..plugins import event_bus

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/recent")
async def recent(_: AdminUser, limit: int = 50):
    return [e.__dict__ for e in event_bus.history[-limit:]][::-1]


@router.post("/publish")
async def publish(_: AdminUser, type: str, payload: dict):
    """Publicar evento manualmente (útil para testar listeners de plugins)."""
    return (await event_bus.publish(type, payload, {"source": "manual"})).__dict__


@router.get("/stream")
async def stream(request: Request, _: CurrentUser):
    queue: asyncio.Queue = asyncio.Queue()

    async def push(event):
        await queue.put(event)
    event_bus.subscribe("*", push)

    async def gen():
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    ev = await asyncio.wait_for(queue.get(), timeout=15)
                    yield f"event: {ev.type}\ndata: {json.dumps(ev.__dict__, default=str)}\n\n"
                except asyncio.TimeoutError:
                    yield ": keep-alive\n\n"
        finally:
            event_bus._subs["*"].remove(push)
    return StreamingResponse(gen(), media_type="text/event-stream")
