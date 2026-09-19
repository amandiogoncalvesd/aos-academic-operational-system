import logging

from ..config import settings

log = logging.getLogger("aos.sms")


async def send_sms(phone: str, message: str) -> bool:
    if settings.ENVIRONMENT in ("development", "test"):
        log.info("[sms:dev] to=%s msg=%s", phone, message)
        return True
    # TODO(prod): Twilio ou gateway local (Unitel/Movicel)
    return False
