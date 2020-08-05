"""Tests for Actor model."""

import datetime as dt

from flask_sqlalchemy import SQLAlchemy
import pytest

from intermine_compose.models.actor import Actor
from ..factories import ActorFactory


@pytest.mark.usefixtures("db")
class TestActorModel:
    """User tests."""

    def test_get_by_id(self: "TestActorModel") -> None:
        """Get user by ID."""
        user = Actor("foo", "foo@bar.com")
        user.save()

        retrieved = Actor.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self: "TestActorModel") -> None:
        """Test creation date."""
        user = Actor(name="foo2", email="foo2@bar.com")
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(self: "TestActorModel") -> None:
        """Test null password."""
        user = Actor(name="foo3", email="foo3@bar.com")
        user.save()
        assert user.password is None

    def test_factory(self: "TestActorModel", db: SQLAlchemy) -> None:
        """Test user factory."""
        user = ActorFactory(password="myprecious")  # noqa
        db.session.commit()
        assert bool(user.name)
        assert bool(user.email)
        assert bool(user.organisation)
        assert bool(user.created_at)
        assert user.check_password("myprecious")

    def test_check_password(self: "TestActorModel") -> None:
        """Check password."""
        password = "foobarbaz123"  # noqa
        user = Actor.create(name="foo4", email="foo4@bar.com", password=password)
        assert user.check_password("foobarbaz123") is True
        assert user.check_password("barfoobaz") is False

    def test_password_reset(self: "TestActorModel") -> None:
        """Test password reset flow."""
        password = "foobarbaz123"  # noqa
        user: Actor = Actor.create(name="foo5", email="foo5@bar.com", password=password)
        token = user.get_reset_password_token()
        retrieved_user = user.verify_reset_password_token(token)
        assert user == retrieved_user
