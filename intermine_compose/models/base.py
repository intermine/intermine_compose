from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime, Column

db = SQLAlchemy()

class TimestampMixin(object):
    created = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)