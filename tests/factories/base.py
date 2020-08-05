"""Base factory."""

from typing import Any, Dict, List

import factory
from factory.alchemy import SQLAlchemyModelFactory

from intermine_compose.extentions import db


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class JSONFactoryMixin(factory.Factory):
    """Overwrites Factory._create() to produce JSON serialized models."""

    @classmethod
    def _create(
        cls: Any, model_class: Any, *args: List[Any], **kwargs: List[Dict[Any, Any]]
    ) -> Any:
        """Override the default ``_create`` with our custom call."""
        schema = model_class()
        results = schema.dumps(kwargs)

        return results


class ObjFactoryMixin(factory.Factory):
    """Overwrites Factory._create() to produce deserialized models."""

    @classmethod
    def _create(
        cls: Any, model_class: Any, *args: List[Any], **kwargs: List[Dict[Any, Any]]
    ) -> Any:
        """Override the default ``_create`` with our custom call."""
        schema = model_class()
        results = schema.dump(kwargs)

        return results
