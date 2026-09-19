from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    sub: str
    jti: str
    role: str
    institution_id: str | None = None
    exp: int
    type: str = "access"


class RefreshToken(BaseModel):
    refresh_token: str
