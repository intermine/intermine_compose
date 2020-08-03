"""Mixins for database models."""

from datetime import datetime
from typing import Any, List, Union

from sqlalchemy import Column, DateTime

from intermine_compose.extentions import db


class TimestampMixin(object):
    """Mixin that adds timestamp."""

    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD operations."""

    @classmethod
    def create(cls: Any, **kwargs: Any) -> Any:
        """Create a new record and save it to the database."""
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def bulk_create(cls: Any, list: List[Any]) -> Any:
        """Create a new records and save them to the database."""
        instance_list: List[Any] = []
        for item in list:
            instance_list.append(cls(**item))
        db.session.bulk_save_objects(instance_list)
        db.session.commit()
        return True

    def update(self: "CRUDMixin", commit: bool = True, **kwargs: Any) -> Any:
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    @classmethod
    def bulk_update(cls: Any, list: List[Any]) -> Any:
        """Create a new records and save them to the database."""
        instance_list: List[Any] = []
        for item in list:
            instance_list.append(cls(**item))
        # for item in list:
        #     for attr, value in item.items():
        #         setattr()
        db.session.bulk_update_mappings(list)
        db.session.commit()
        return instance_list

    def save(self: "CRUDMixin", commit: bool = True) -> Any:
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self: "CRUDMixin", commit: bool = True) -> Union[bool, Any]:
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """Adds a surrogate int 'primary key' column named ``id`` to any orm class."""

    __table_args__ = {"extend_existing": True}

    id = Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls: Any, record_id: Union[str, int]) -> Union[None, Any]:
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, str) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None
