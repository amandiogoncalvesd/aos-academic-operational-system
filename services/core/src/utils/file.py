import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

UPLOAD_DIR = Path("uploads")
ALLOWED = {"image/png", "image/jpeg", "image/webp", "application/pdf", "text/csv"}


def validate_file_type(file: UploadFile, allowed: set[str] | None = None) -> None:
    if file.content_type not in (allowed or ALLOWED):
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Tipo não suportado: {file.content_type}")


async def save_upload_file(file: UploadFile, subdir: str = "misc") -> str:
    validate_file_type(file)
    dest = UPLOAD_DIR / subdir
    dest.mkdir(parents=True, exist_ok=True)
    ext = Path(file.filename or "").suffix
    name = f"{uuid.uuid4()}{ext}"
    (dest / name).write_bytes(await file.read())
    return f"{subdir}/{name}"


def generate_file_url(path: str) -> str:
    return f"/static/{path}"
