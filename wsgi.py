"""WSGI interface."""

import uvicorn

from intermine_compose.app import create_app
from intermine_compose.extentions import settings


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        app, host=settings.APP_HOST, port=settings.APP_PORT, log_level=settings.APP_LOG,
    )
