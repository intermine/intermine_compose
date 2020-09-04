"""User API."""

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response

from intermine_compose.database import get_db
from intermine_compose.extentions import get_user
from intermine_compose.models.actor import Actor
from intermine_compose.routes.user_schema import (
    UserProfileSchema,
    UserRegisterSchema,
    UserUpdateSchema,
)

user_router = APIRouter()


@user_router.post(
    "/",
    tags=["user", "auth"],
    dependencies=[Depends(get_db)],
    response_model=UserProfileSchema,
)
async def register(user_register_form: UserRegisterSchema) -> Response:
    """Register user."""
    # Create user if checks are passed
    try:
        actor: Actor = Actor.create(**user_register_form.dict())
        actor.set_password(actor.password)
        actor.save()
    except BaseException as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))
    return actor


@user_router.get(
    "/",
    tags=["user"],
    dependencies=[Depends(get_user)],
    response_model=UserProfileSchema,
)
# @login_required
async def get_profile(user: Actor = Depends(get_user)) -> Response:
    """Get user profile."""
    return user


@user_router.patch(
    "/",
    tags=["user"],
    dependencies=[Depends(get_user)],
    response_model=UserProfileSchema,
)
# @login_required
async def update_profile(
    user_update_form: UserUpdateSchema, user: Actor = Depends(get_user)
) -> Response:
    """Get user profile."""
    user_update_form_dict = user_update_form.dict(exclude_unset=True)
    user.update(**user_update_form_dict).execute()
    user = Actor.get_by_id(user.get_id())
    return user
