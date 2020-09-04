"""Auth API."""

from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from peewee import PeeweeException

from intermine_compose.database import get_db
from intermine_compose.extentions import get_user, settings
from intermine_compose.models import Actor
from intermine_compose.routes.auth_schemas import (
    AuthLoginSchema,
    AuthResetPasswordRequest,
    AuthResetPasswordSchema,
    AuthPasswordUpdateSchema,
)
from intermine_compose.routes.common_schema import SuccessSchema
from intermine_compose.routes.user_schema import UserProfileSchema


auth_router = APIRouter()


@auth_router.post(
    "/login/",
    tags=["user", "auth"],
    dependencies=[Depends(get_db)],
    response_model=UserProfileSchema,
)
async def login(auth_login_form: AuthLoginSchema, response: Response) -> Response:
    """Login user."""
    try:
        user_list: List[Actor] = Actor.select().where(
            Actor.email == auth_login_form.email
        )
        if len(user_list) == 0:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    except PeeweeException:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    try:
        status = user_list[0].check_password(auth_login_form.password)
    except BaseException:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

    if status is not True:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

    token = user_list[0].create_access_token()

    response.set_cookie(
        key=settings.API_KEY_NAME,
        value=f"Bearer {token}",
        domain=settings.COOKIE_DOMAIN,
        httponly=True,
        max_age=(settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60),
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )

    return user_list[0]


@auth_router.get("/logout/", tags=["auth"])
async def logout_and_remove_cookie() -> Response:
    """Logout user and remove cookie."""
    response = RedirectResponse(url="/")
    response.delete_cookie(settings.API_KEY_NAME, domain=settings.COOKIE_DOMAIN)
    return response


@auth_router.post(
    "/password/reset_request/",
    tags=["auth"],
    dependencies=[Depends(get_db)],
    response_model=SuccessSchema,
)
async def reset_password_request(
    reset_password_request_form: AuthResetPasswordRequest,
) -> Response:
    """Reset password request."""
    try:
        user = Actor.get(Actor.email == reset_password_request_form.email)
    except PeeweeException:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    if user is not None:
        pass
    return {"detail": "OK"}


@auth_router.post(
    "/password/reset/",
    tags=["auth"],
    dependencies=[Depends(get_db)],
    response_model=SuccessSchema,
)
async def reset_password(reset_password_form: AuthResetPasswordSchema) -> Response:
    """Reset password."""
    try:
        user = Actor.verify_reset_password_token(reset_password_form.reset_token)
    except PeeweeException:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    if user is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

    user.set_password(reset_password_form.password)
    user.save()
    return {"detail": "OK"}


@auth_router.put(
    "/password/",
    tags=["auth"],
    dependencies=[Depends(get_db)],
    response_model=SuccessSchema,
)
async def update_password(
    auth_password_update_form: AuthPasswordUpdateSchema, user: Actor = Depends(get_user)
) -> Response:
    """Update password."""
    user.update(**auth_password_update_form).execute()
    user.set_password(user.password)
    user.save()
    return {"detail": "OK"}
