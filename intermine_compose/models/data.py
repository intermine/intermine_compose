from .base import db, TimestampMixin
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields
from uuid import uuid4

class DataFile(TimestampMixin, db.Model):
    fileId = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    # fileFormat = Column(String, nullable=False)
    # organisms = Column(String(), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="data_files", lazy="joined", single_parent=True)
    mine_id = Column(UUID(as_uuid=True), ForeignKey("mine.id"))
    mine = relationship("Mine", back_populates="data_files", lazy="joined", single_parent=True)

class DataFileSchema(Schema):
    fileId = fields.UUID(required=True)
    name = fields.String(required=True)
    # fileFormat = fields.String(required=True)
    # organisms = fields.String(required=True)

class DataFileUploadSchema(Schema):
    mineId = fields.UUID(required=True)

class DataFileRemoteUploadSchema(Schema):
    mineId = fields.UUID(required=True)
    remoteURL = fields.Url(required=True)