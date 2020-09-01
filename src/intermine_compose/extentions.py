"""App extenstions."""

from http import HTTPStatus
from typing import Optional

from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyCookie, APIKeyHeader, APIKeyQuery
from jose import JWTError
from passlib.context import CryptContext
from playhouse.postgres_ext import PostgresqlExtDatabase
from sendgrid import SendGridAPIClient

from intermine_compose.config import get_config

# initialize config
settings = get_config()

sendGrid: SendGridAPIClient = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

origins = ["http://localhost", "http://localhost:9991", "https://cloud.intermine.org"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

api_key_query = APIKeyQuery(name=settings.API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=settings.API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
) -> Optional[str]:
    """Validate credentials."""
    if api_key_query is not None:
        return api_key_query
    elif api_key_header is not None:
        return api_key_header
    elif api_key_cookie is not None:
        return api_key_cookie
    else:
        return None


# Hack to get around circular import
from intermine_compose.database import get_db  # noqa
from intermine_compose.models import Actor  # noqa


async def get_user(
    token: str = Depends(get_api_key), db: PostgresqlExtDatabase = Depends(get_db)
) -> Actor:
    """Extract user."""
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token is None:
        raise credentials_exception

    try:
        user = Actor.verify_access_token(token.split(" ")[1])
    except JWTError:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    return user
