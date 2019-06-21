from .base import db
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

class User(db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True)
    firstname = Column(String(80))
    lastname = Column(String(80))
    organization = Column(String(80))
    email = Column(String(120), unique=True, nullable=False)