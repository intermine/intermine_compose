from .base import db, ma, TimestampMixin
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from marshmallow import fields, validate, post_load
from uuid import uuid4
from flask_login import UserMixin

# User class for storing user data in database
class User(TimestampMixin, UserMixin, db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    firstName = Column(String(80))
    lastName = Column(String(80))
    organisation = Column(String(80))
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(1000), nullable=False)
    mines = relationship("Mine", back_populates="user", lazy="joined")
    active_mine_quota = Column(Integer, default=1)
    inactive_mine_quota = Column(Integer, default=5)
    daily_mine_build_quota = Column(Integer, default=5)
    storage_quota = Column(Integer, default=500)

# User login schema for validating login data
class UserCredentialsSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


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