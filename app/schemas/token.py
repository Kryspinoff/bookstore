from datetime import timedelta

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    exp: timedelta
    sub: str
    role: str = None
