from .base import db, TimestampMixin
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class Mine(TimestampMixin, db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True)
    url = Column(String(100), nullable=False)
    config = Column(String(5000), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True)
    user = relationship("User", back_populates="mines", lazy="joined", single_parent=True)