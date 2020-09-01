"""Status API."""

from fastapi import APIRouter
from fastapi import Response

status_router = (
    APIRouter()
)  # Blueprint("status", __name__, url_prefix='/api/v1/status')


@status_router.get("/", tags=["status"])
async def status() -> Response:
    """Get app status."""
    return {"message": "OK"}
