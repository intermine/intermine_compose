"""Intermine Compose App."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logzero import logger

from intermine_compose.extentions import origins
from intermine_compose.routes import (
    auth_router,
    # build_bp,
    # configurator_bp,
    # data_bp,
    status_router,
    # mine_bp,
    user_router,
)


def create_app() -> FastAPI:
    """App factory."""
    app = FastAPI()  # Flask(__name__, template_folder="./templates")
    logger.info("App instance created")

    # Register app middlewares
    register_middlewares(app)
    logger.debug("Middlewares loaded")

    # register routers
    register_routers(app)
    logger.debug("Routers registered")

    return app


def register_middlewares(app: FastAPI) -> None:
    """Register FastAPI middlewares."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_routers(app: FastAPI) -> None:
    """Register Flask blueprints."""
    app.include_router(auth_router, prefix="/v1/auth", tags=["auth"])
    app.include_router(user_router, prefix="/v1/auth", tags=["user"])
    app.include_router(status_router, prefix="/v1/status", tags=["status"])
    # app.register_blueprint(configurator_bp)
    # app.register_blueprint(data_bp)
    # app.register_blueprint(mine_bp)
    # app.register_blueprint(build_bp)
    return None
