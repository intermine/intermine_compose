"""Status API."""

from fastapi import APIRouter
from fastapi import Response

status_router = APIRouter()


@status_router.get("/", tags=["status"])
async def status() -> Response:
    """Get app status."""
    return {"message": "OK"}
