from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime, Column
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()

class TimestampMixin(object):
    created = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)