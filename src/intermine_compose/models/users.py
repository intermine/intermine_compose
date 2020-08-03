"""User model."""

import os
from time import time
from uuid import uuid4

from flask_login import UserMixin
import jwt
from marshmallow import fields, validate
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from intermine_compose.extentions import db, ma
from intermine_compose.models.meta.mixins import Model, SurrogatePK, TimestampMixin

# User class for storing user data in database
class User(TimestampMixin, UserMixin, SurrogatePK, Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    firstName = Column(String(80))
    lastName = Column(String(80))
    organisation = Column(String(80))
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(1000), nullable=False)
    mines = relationship("Mine", back_populates="user", lazy="joined")
    data_files = relationship("DataFile", back_populates="user", lazy="joined")
    builds = relationship("Build", back_populates="user", lazy="joined")
    active_mine_quota = Column(Integer, default=1)
    inactive_mine_quota = Column(Integer, default=5)
    daily_mine_build_quota = Column(Integer, default=5)
    storage_quota = Column(Integer, default=500)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": str(self.id), "exp": time() + expires_in},
            os.environ.get("SECRET_KEY"),
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])[
                "reset_password"
            ]
        except:
            return
        return User.query.filter_by(id=id)


# User login schema for validating login data
class UserCredentialsSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


# User forgot password schema to validate email input
class UserForgotPasswordSchema(ma.Schema):
    email = fields.Email(required=True, validate=validate.Length(max=120))


# User reset password schema to validate reset token and password input
class UserResetPasswordSchema(ma.Schema):
    reset_token = fields.Str(required=True, validate=validate.Length(max=1000))
    password = fields.Str(required=True, validate=validate.Length(max=1000))


# User registration schema for validating User registration
class UserRegisterSchema(ma.Schema):
    email = fields.Email(required=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    organisation = fields.Str(required=True)
    password = fields.Str(required=True)


# Slim User schema for sending user data to clients
class SlimUserSchema(ma.Schema):
    email = fields.Email(required=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    organisation = fields.Str(required=True)


class UserProfileSchema(ma.Schema):
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    organisation = fields.Str(required=True)
