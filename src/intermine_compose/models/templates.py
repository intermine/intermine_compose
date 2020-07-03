from .base import db, TimestampMixin
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class Template(TimestampMixin, db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    data = Column(String, nullable=False)