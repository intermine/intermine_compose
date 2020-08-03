"""Template model."""

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from intermine_compose.extentions import db, ma
from intermine_compose.models.meta.mixins import Model, TimestampMixin


class Template(TimestampMixin, Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    data = Column(String, nullable=False)
