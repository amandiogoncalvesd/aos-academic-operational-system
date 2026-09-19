from fastapi import FastAPI

from ..config import settings as app_settings
from . import audit_logs, auth, events, health, institutions, notifications, plugins, roles, settings, users


def include_routers(app: FastAPI) -> None:
    for r in (auth, users, institutions, roles, notifications, audit_logs, plugins, settings, events):
        app.include_router(r.router, prefix=app_settings.API_PREFIX)
    app.include_router(health.router)  # /health sem prefixo (probes k8s)
