from .base import db, TimestampMixin
from sqlalchemy import Column, String,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class User(TimestampMixin, db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True)
    firstname = Column(String(80))
    lastname = Column(String(80))
    organization = Column(String(80))
    email = Column(String(120), unique=True, nullable=False)
    pwd_hash = Column(String(80), nullable=False)
    mines = relationship("Mine", back_populates="user", lazy="joined")
    active_mine_quota = Column(Integer, default=1)
    inactive_mine_quota = Column(Integer, default=5)
    daily_mine_build_quota = Column(Integer, default=5)
    storage_quota = Column(Integer, default=500)