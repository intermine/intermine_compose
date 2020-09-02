"""Tests for Actor model."""

import datetime as dt

from playhouse.postgres_ext import PostgresqlExtDatabase

from intermine_compose.models.actor import Actor
from ..factories import ActorFactory


class TestActorModel:
    """User tests."""

    def test_get_by_id(self: "TestActorModel", db: PostgresqlExtDatabase) -> None:
        """Get user by ID."""
        user = Actor(name="foo", email="foo@bar.com")
        user.save()

        retrieved = Actor.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(
        self: "TestActorModel", db: PostgresqlExtDatabase
    ) -> None:
        """Test creation date."""
        user = Actor(name="foo2", email="foo2@bar.com")
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(
        self: "TestActorModel", db: PostgresqlExtDatabase
    ) -> None:
        """Test null password."""
        user = Actor(name="foo3", email="foo3@bar.com")
        user.save()
        assert user.password is None

    def test_factory(self: "TestActorModel", db: PostgresqlExtDatabase) -> None:
        """Test user factory."""
        user = ActorFactory(password="myprecious")  # noqa
        assert bool(user.name)
        assert bool(user.email)
        assert bool(user.organisation)
        assert bool(user.created_at)
        assert user.check_password("myprecious")

    def test_check_password(self: "TestActorModel", db: PostgresqlExtDatabase) -> None:
        """Check password."""
        password = "foobarbaz123"  # noqa
        user = Actor(name="foo4", email="foo4@bar.com", password=password)
        user.set_password(user.password)
        user.save()
        assert user.check_password(password) is True
        assert user.check_password("barfoobaz") is False

    def test_password_reset(self: "TestActorModel", db: PostgresqlExtDatabase) -> None:
        """Test password reset flow."""
        password = "foobarbaz123"  # noqa
        user: Actor = Actor(name="foo5", email="foo5@bar.com", password=password)
        user.save()
        token = user.create_reset_password_token()
        retrieved_user = user.verify_reset_password_token(token)
        assert user == retrieved_user
