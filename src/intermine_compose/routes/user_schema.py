# User login schema for validating login data
"""Schemas for user API."""

from marshmallow import fields, Schema, validate, validates, ValidationError

from intermine_compose.models.actor import Actor


class UserLogin(Schema):
    """Login form."""

    email = fields.String(required=True, validate=validate.Length(max=80))
    password = fields.Str(required=True, validate=validate.Length(max=80))


class ResetPassword(Schema):
    """Reset password form."""

    reset_token = fields.String(required=True, validate=validate.Length(max=500))
    password = fields.String(required=True, validate=validate.Length(max=80))


class ResetPasswordRequest(Schema):
    """Reset password request form."""

    email = fields.String(required=True, validate=validate.Length(max=80))


# User registration schema for validating User registration
class UserRegister(Schema):
    """Register form schema."""

    firstName = fields.Str(required=False)
    lastName = fields.Str(required=False)
    name = fields.Str(required=False, validate=validate.Length(max=80))
    email = fields.Str(required=True, validate=validate.Length(max=80))
    organisation = fields.Str(required=False, validate=validate.Length(max=80))
    password = fields.Str(required=True, validate=validate.Length(max=80))

    @validates("email")
    def check_email(self: "UserRegister", value: str) -> None:
        """Checks if email is already present."""
        user = Actor.query.filter_by(email=value).first()
        if user is not None:
            raise ValidationError("email is already present")


class UserProfile(Schema):
    """User profile schema."""

    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    name = fields.Str(required=True, validate=validate.Length(max=80))
    email = fields.Str(required=True, validate=validate.Length(max=80))
    organisation = fields.Str(required=False, validate=validate.Length(max=80))
    created_at = fields.String(required=True, validate=validate.Length(max=80))
    updated_at = fields.String(
        required=False, validate=validate.Length(max=80), allow_none=True
    )


class SlimUserProfile(Schema):
    """User profile schema."""

    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    name = fields.Str(required=True, validate=validate.Length(max=80))
    organisation = fields.Str(required=False, validate=validate.Length(max=80))
    created_at = fields.String(required=True, validate=validate.Length(max=80))
    updated_at = fields.String(
        required=False, validate=validate.Length(max=80), allow_none=True
    )
