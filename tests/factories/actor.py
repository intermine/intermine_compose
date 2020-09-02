"""Actor factory."""

from typing import Any

from factory import Factory, Faker, post_generation

from intermine_compose.models.actor import Actor
from intermine_compose.routes.user_schema import UserRegisterSchema
from .base import ObjFactoryMixin, PeeweeModelFactory


class ActorFactory(PeeweeModelFactory):
    """User factory."""

    class Meta:
        """Factory configuration."""

        model = Actor

    name = Faker("name")
    email = Faker("email")
    organisation = Faker("company")
    password = Faker("password")

    @post_generation
    def hash_password(
        obj: Actor, create: Any, extracted: Any, **kwargs: Any  # noqa
    ) -> None:  # noqa
        obj.set_password(obj.password)
        obj.save()


class UserRegisterSchemaFactory(Factory):
    """Register factory."""

    class Meta:
        """Factory configuration."""

        model = UserRegisterSchema

    name = Faker("name")
    email = Faker("email")
    password = Faker("password")
    organisation = Faker("company")


class UserRegisterSchemaObjFactory(UserRegisterSchemaFactory, ObjFactoryMixin):
    """Register obj factory."""
