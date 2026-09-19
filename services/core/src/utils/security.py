import hashlib
import secrets

import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def generate_random_token(nbytes: int = 32) -> str:
    return secrets.token_urlsafe(nbytes)


def generate_otp(digits: int = 6) -> str:
    return "".join(str(secrets.randbelow(10)) for _ in range(digits))


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
