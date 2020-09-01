"""App extenstions."""

from http import HTTPStatus

from fastapi import HTTPException, Response, Security
from fastapi.security.api_key import APIKeyCookie, APIKeyHeader, APIKeyQuery
from passlib.context import CryptContext
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
) -> Response:
    """Validate credentials."""
    if api_key_query == settings.API_KEY:
        return api_key_query
    elif api_key_header == settings.API_KEY:
        return api_key_header
    elif api_key_cookie == settings.API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Could not validate credentials"
        )
