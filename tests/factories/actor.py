"""Actor factory."""

from factory import Factory, Faker, PostGenerationMethodCall

from intermine_compose.models.actor import Actor
from intermine_compose.routes.user_schema import UserRegister
from .base import BaseFactory, ObjFactoryMixin


class ActorFactory(BaseFactory):
    """User factory."""

    name = Faker("name")
    email = Faker("email")
    organisation = Faker("company")
    password = PostGenerationMethodCall("set_password", "example")

    class Meta:
        """Factory configuration."""

        model = Actor


class RegisterSchemaFactory(Factory):
    """Register factory."""

    name = Faker("name")
    email = Faker("email")
    password = Faker("password")
    organisation = Faker("company")

    class Meta:
        """Factory configuration."""

        model = UserRegister


class RegisterSchemaObjFactory(RegisterSchemaFactory, ObjFactoryMixin):
    """Register obj factory."""
