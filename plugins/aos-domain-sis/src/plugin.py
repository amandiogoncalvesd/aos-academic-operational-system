"""Plugin aos-domain-sis — regista modelos, rotas e hooks."""
import logging

from .models import Course, Enrollment
from .routes import router

log = logging.getLogger("aos.plugin.sis")


def register(ctx):
    ctx.add_models(Course, Enrollment)  # importados → entram no Base.metadata (create_all / alembic)
    ctx.add_router(router)

    @ctx.on_event("auth.user.registered")
    async def on_user(event):
        if event.payload.get("role") == "student":
            log.info("novo estudante %s — pronto para matrícula", event.payload["email"])

    @ctx.filter("sis.enrollment.validate", priority=5)
    def block_inactive_course(verdict, course, student_id):
        if not course.is_active:
            return {"ok": False, "reason": "Curso inactivo"}
        return verdict
