# User login schema for validating login data
"""Schemas for user API."""

from http import HTTPStatus
from typing import Any, Optional

from fastapi import HTTPException
from pydantic import BaseModel, ValidationError, validator

from intermine_compose.database import PeeweeGetterDict
from intermine_compose.models.actor import Actor


class UserLoginSchema(BaseModel):
    """Login Schema."""

    email: str
    password: str


class ResetPasswordSchema(BaseModel):
    """Reset password schema."""

    reset_token: str  # fields.String(required=True, validate=validate.Length(max=500))
    password: str  # fields.String(required=True, validate=validate.Length(max=80))


class ResetPasswordRequest(BaseModel):
    """Reset password schema."""

    email: str  # fields.String(required=True, validate=validate.Length(max=80))


# User registration schema for validating User registration
class UserSlimSchema(BaseModel):
    """User base."""

    firstName: Optional[str]
    lastName: Optional[str]
    name: str
    email: str
    organisation: str


class UserRegisterSchema(UserSlimSchema):
    """User register schema."""

    password: str

    @validator("email")
    def check_email(cls: "UserRegisterSchema", value: str) -> None:
        """Checks if email is already present."""
        user_list = Actor.select().where(Actor.email == value)
        if len(user_list) != 0:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, detail="email is already present"
            )
        return value


class UserProfileSchema(UserSlimSchema):
    """user profile schema."""

    created_at: Any
    updated_at: Optional[Any]
    active: bool

    class Config:
        """Config."""

        orm_mode = True
        getter_dict = PeeweeGetterDict
