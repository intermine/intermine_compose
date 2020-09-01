"""User API."""

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security.api_key import APIKey

from intermine_compose.database import get_db
from intermine_compose.extentions import get_api_key
from intermine_compose.models.actor import Actor
from intermine_compose.routes.user_schema import (
    UserProfileSchema,
    UserRegisterSchema,
)

user_router = APIRouter()


@user_router.post(
    "/register/",
    tags=["user", "auth"],
    dependencies=[Depends(get_db)],
    response_model=UserProfileSchema,
)
async def register(user_register_form: UserRegisterSchema) -> Response:
    """Register user."""

    # Create user if checks are passed
    try:
        actor = Actor.create(**user_register_form.dict())
    except BaseException as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    return actor


@user_router.get(
    "/profile/",
    tags=["user"],
    dependencies=[Depends(get_db)],
    response_model=UserProfileSchema,
)
# @login_required
async def get_profile(api_key: APIKey = Depends(get_api_key)):
    """Get user profile."""
    pass
