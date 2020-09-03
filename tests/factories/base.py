"""Base factory."""

from typing import Any, Dict, List

import factory


class PeeweeModelFactory(factory.Factory):
    """Peewee Model Factory."""

    class Meta:
        """Meta."""

        abstract = True

    @classmethod
    def _build(
        cls: "PeeweeModelFactory", model_class: Any, *args: Any, **kwargs: Any
    ) -> Any:
        return model_class(*args, **kwargs)

    @classmethod
    def _create(
        cls: "PeeweeModelFactory",
        model_class: Any,
        *args: List[Any],
        **kwargs: List[Dict[Any, Any]]
    ) -> Any:
        """Create an instance of the model, and save it to the database."""
        obj = model_class.create(*args, **kwargs)
        return obj


class BaseFactory(PeeweeModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True


class JSONFactoryMixin(factory.Factory):
    """Overwrites Factory._create() to produce JSON serialized models."""

    @classmethod
    def _build(cls: Any, model_class: Any, *args: Any, **kwargs: Any) -> Any:
        return model_class.construct(*args, **kwargs).json()

    @classmethod
    def _create(
        cls: Any, model_class: Any, *args: List[Any], **kwargs: List[Dict[Any, Any]]
    ) -> Any:
        """Override the default ``_create`` with our custom call."""
        return model_class(*args, **kwargs).json()


class ObjFactoryMixin(factory.Factory):
    """Overwrites Factory._create() to produce deserialized models."""

    @classmethod
    def _build(cls: Any, model_class: Any, *args: Any, **kwargs: Any) -> Any:
        return model_class.construct(*args, **kwargs).dict()

    @classmethod
    def _create(
        cls: Any, model_class: Any, *args: List[Any], **kwargs: List[Dict[Any, Any]]
    ) -> Any:
        """Override the default ``_create`` with our custom call."""
        return model_class(*args, **kwargs).dict()
