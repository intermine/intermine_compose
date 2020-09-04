"""Tests for User API."""

from fastapi.testclient import TestClient
from playhouse.shortcuts import model_to_dict
import pytest
from requests.cookies import RequestsCookieJar

from intermine_compose.models.actor import Actor
from intermine_compose.routes.user_schema import UserProfileSchema
from ..factories import UserRegisterSchemaObjFactory


@pytest.mark.usefixtures("db")
def test_can_register(testclient: TestClient) -> None:
    """Register a new user."""
    old_count = len(Actor.select())
    for _ in range(0, 10):
        params = UserRegisterSchemaObjFactory()
        res = testclient.post(url="/v1/user/", json=params)
        assert res.status_code == 200
    # new users created
    assert len(Actor.select()) == old_count + 10


@pytest.mark.usefixtures("db")
def test_sees_error_message_if_user_already_registered(
    user: Actor, testclient: TestClient
) -> None:
    """Show error if user already registered."""
    params = UserRegisterSchemaObjFactory.build(email=user.email)
    res = testclient.post(url="/v1/user/", json=params)
    # sees error
    assert "email is already present" in str(res.json())


def test_can_get_profile(
    user: Actor, testclient: TestClient, cookie_jar: RequestsCookieJar
) -> None:
    """Show error if user already registered."""
    res = testclient.get(url="/v1/user/", cookies=cookie_jar)
    assert res.status_code == 200
    user_get = UserProfileSchema(**res.json())
    user_get_dict = user_get.dict(exclude_unset=True)
    user_dict = model_to_dict(user)

    # remove timestamps to pass tests
    # timestamps are stored in db in different format
    user_get_dict.pop("created_at")
    user_get_dict.pop("updated_at")
    for key in user_get_dict:
        assert user_get_dict[key] == user_dict[key]


def test_can_update_profile(
    user: Actor, testclient: TestClient, cookie_jar: RequestsCookieJar
) -> None:
    """Show error if user already registered."""
    assert user.name == "bruce"
    params = dict(name="stark")
    res = testclient.patch(url="/v1/user/", json=params, cookies=cookie_jar)
    assert res.status_code == 200
    user_get = UserProfileSchema(**res.json())
    user_get_dict = user_get.dict(exclude_unset=True)
    user_dict = model_to_dict(user)
    assert user_get_dict["name"] == params["name"]
    assert user_get_dict["name"] != user_dict["name"]
