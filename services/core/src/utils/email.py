"""Envio de email. Em dev apenas regista no log; em prod ligar SMTP/SendGrid."""
import logging

from ..config import settings

log = logging.getLogger("aos.email")


async def send_email(to: str, subject: str, template: str, context: dict | None = None) -> bool:
    if settings.ENVIRONMENT in ("development", "test"):
        log.info("[email:dev] to=%s subject=%s template=%s ctx=%s", to, subject, template, context)
        return True
    # TODO(prod): implementar SMTP (aiosmtplib) ou SendGrid via httpx
    log.warning("send_email não configurado em produção")
    return False
