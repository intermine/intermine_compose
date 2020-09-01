"""Auth schemas."""

from pydantic import BaseModel


class AuthLoginSchema(BaseModel):
    """Login Schema."""

    email: str
    password: str
