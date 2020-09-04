"""Common schemas."""

from pydantic import BaseModel


class SuccessSchema(BaseModel):
    """Success Schema."""

    detail: str


class ErrorSchema(BaseModel):
    """Error Schema."""

    detail: str
