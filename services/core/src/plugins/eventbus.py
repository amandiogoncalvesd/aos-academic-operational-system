"""AOS Event Bus — pub/sub com backends memory (dev/test), redis, kafka.

Todos os eventos têm formato canónico AOSEvent e nomes `dominio.entidade.acao`
(ex.: auth.user.registered, sis.student.enrolled, lms.grade.submitted).
"""
from __future__ import annotations

import asyncio
import fnmatch
import json
import logging
import uuid
from collections import defaultdict
from collections.abc import Awaitable, Callable
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

log = logging.getLogger("aos.eventbus")
Handler = Callable[["AOSEvent"], Awaitable[None] | None]


@dataclass
class AOSEvent:
    type: str
    payload: dict
    metadata: dict = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: str = "1.0"

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str)

    @classmethod
    def from_json(cls, raw: str | bytes) -> AOSEvent:
        return cls(**json.loads(raw))


class EventBus:
    """Backend em memória. Suporta wildcards (`sis.*`, `*`)."""

    def __init__(self) -> None:
        self._subs: dict[str, list[Handler]] = defaultdict(list)
        self.history: list[AOSEvent] = []  # mini event-store (dev); em prod → Kafka/Postgres
        self.max_history = 1000

    def subscribe(self, event_types: str | list[str], handler: Handler) -> None:
        for et in [event_types] if isinstance(event_types, str) else event_types:
            self._subs[et].append(handler)
            log.debug("subscribed %s -> %s", et, getattr(handler, "__name__", handler))

    def on(self, *event_types: str):
        def deco(fn: Handler) -> Handler:
            self.subscribe(list(event_types), fn)
            return fn
        return deco

    def _matching_handlers(self, event_type: str) -> list[Handler]:
        out: list[Handler] = []
        for pattern, handlers in self._subs.items():
            if pattern == event_type or fnmatch.fnmatch(event_type, pattern):
                out.extend(handlers)
        return out

    async def publish(self, event_type: str, payload: dict, metadata: dict | None = None) -> AOSEvent:
        event = AOSEvent(type=event_type, payload=payload, metadata=metadata or {})
        self.history.append(event)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        await self._dispatch(event)
        return event

    async def _dispatch(self, event: AOSEvent) -> None:
        for h in self._matching_handlers(event.type):
            try:
                res = h(event)
                if asyncio.iscoroutine(res):
                    await res
            except Exception:  # um listener nunca derruba o publisher
                log.exception("listener %s falhou em %s", getattr(h, "__name__", h), event.type)

    def subscriptions(self) -> dict[str, list[str]]:
        return {k: [getattr(h, "__name__", str(h)) for h in v] for k, v in self._subs.items()}

    async def start(self) -> None: ...
    async def stop(self) -> None: ...


class RedisEventBus(EventBus):
    """Pub/Sub via Redis (canal aos.events). Boa opção antes de Kafka."""

    CHANNEL = "aos.events"

    def __init__(self, url: str) -> None:
        super().__init__()
        self._url = url
        self._redis = None
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        import redis.asyncio as aioredis

        self._redis = aioredis.from_url(self._url)
        pubsub = self._redis.pubsub()
        await pubsub.subscribe(self.CHANNEL)

        async def _listen():
            async for msg in pubsub.listen():
                if msg.get("type") == "message":
                    await self._dispatch(AOSEvent.from_json(msg["data"]))

        self._task = asyncio.create_task(_listen())
        log.info("RedisEventBus ligado a %s", self._url)

    async def publish(self, event_type, payload, metadata=None):
        event = AOSEvent(type=event_type, payload=payload, metadata=metadata or {})
        self.history.append(event)
        await self._redis.publish(self.CHANNEL, event.to_json())  # dispatch ocorre no listener
        return event

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
        if self._redis:
            await self._redis.aclose()


class KafkaEventBus(EventBus):
    """Kafka (tópico aos.events) via aiokafka. Persistente, replay, alta vazão."""

    TOPIC = "aos.events"

    def __init__(self, bootstrap: str) -> None:
        super().__init__()
        self._bootstrap = bootstrap
        self._producer = None
        self._consumer = None
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

        self._producer = AIOKafkaProducer(bootstrap_servers=self._bootstrap)
        self._consumer = AIOKafkaConsumer(self.TOPIC, bootstrap_servers=self._bootstrap, group_id="aos-core")
        await self._producer.start()
        await self._consumer.start()

        async def _listen():
            async for msg in self._consumer:
                await self._dispatch(AOSEvent.from_json(msg.value))

        self._task = asyncio.create_task(_listen())
        log.info("KafkaEventBus ligado a %s", self._bootstrap)

    async def publish(self, event_type, payload, metadata=None):
        event = AOSEvent(type=event_type, payload=payload, metadata=metadata or {})
        await self._producer.send_and_wait(self.TOPIC, event.to_json().encode(), key=event_type.encode())
        return event

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
        if self._producer:
            await self._producer.stop()
        if self._consumer:
            await self._consumer.stop()


def build_event_bus(backend: str, redis_url: str, kafka_bootstrap: str) -> EventBus:
    if backend == "redis":
        return RedisEventBus(redis_url)
    if backend == "kafka":
        return KafkaEventBus(kafka_bootstrap)
    return EventBus()
