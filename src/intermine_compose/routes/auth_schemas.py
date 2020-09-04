"""Auth schemas."""

from pydantic import BaseModel


class AuthLoginSchema(BaseModel):
    """Login Schema."""

    email: str
    password: str


class AuthPasswordUpdateSchema(BaseModel):
    """Login Schema."""

    password: str


class AuthResetPasswordSchema(BaseModel):
    """Reset password schema."""

    reset_token: str
    password: str


class AuthResetPasswordRequest(BaseModel):
    """Reset password schema."""

    email: str
