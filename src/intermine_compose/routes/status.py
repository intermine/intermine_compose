"""Status API."""

from fastapi import APIRouter
from fastapi import Response

status_route = APIRouter()  # Blueprint("status", __name__, url_prefix='/api/v1/status')


@status_route.get("/", tags=["status"])
async def status() -> Response:
    """Get app status."""
    return {"message": "OK"}
