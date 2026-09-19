"""Plugin aos-core-notify — escuta eventos e gera notificações in-app."""
import logging

from src.database import AsyncSessionLocal
from src.models import Notification

log = logging.getLogger("aos.plugin.notify")


def register(ctx):
    @ctx.on_event("auth.user.registered")
    async def welcome(event):
        title, msg = await ctx.engine.apply_filters(
            "notify.message.render", ("Bem-vindo ao AOS", "A sua conta foi criada. Explore o seu portal."), event)
        async with AsyncSessionLocal() as db:
            db.add(Notification(user_id=event.payload["user_id"], type="success", title=title, message=msg,
                                data={"event": event.type}))
            await db.commit()
        log.info("notificação de boas-vindas → %s", event.payload["email"])

    @ctx.on_event("sis.student.enrolled")
    async def enrolled(event):
        async with AsyncSessionLocal() as db:
            db.add(Notification(user_id=event.payload["user_id"], type="info", title="Matrícula confirmada",
                                message=f"Está inscrito em {event.payload.get('course_name', 'um curso')}.",
                                data=event.payload))
            await db.commit()
