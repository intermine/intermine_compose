from .base import db, TimestampMixin
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields
from uuid import uuid4

class Build(TimestampMixin, db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    buildStatus = Column(String(100), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="builds", lazy="joined", single_parent=True)
    mineId = Column(UUID(as_uuid=True), ForeignKey("mine.id"))
    mine = relationship("Mine", back_populates="builds", lazy="joined", single_parent=True)


class BuildStatusSchema(Schema):
    mineId = fields.String(required=True)
    buildStatus = fields.String(required=True)
    errorDetails = fields.String(required=False)

class BuildTriggerSchema(Schema):
    mineId = fields.String(required=True)