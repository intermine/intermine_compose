"""Intermine Compose App."""

from typing import Any

from fastapi import FastAPI, Request, Response
from flask import Flask
from logzero import logger

from intermine_compose.database import db
from intermine_compose.extentions import bcrypt, cors, login_manager, migrate
from intermine_compose.routes import (
    # build_bp,
    # configurator_bp,
    # data_bp,
    status_route,
    # mine_bp,
    # user_bp,
)


def create_app() -> Flask:
    """App factory."""
    app = FastAPI()  # Flask(__name__, template_folder="./templates")
    logger.info("App instance created")

    # Register app middlewares

    # db session handler
    @app.middleware("http")
    async def db_session_handler(request: Request, call_next: Any) -> Response:
        db.connect()
        response = await call_next(request)
        db.close()
        return response

    logger.debug("Middlewares loaded")

    # register routers
    register_routers(app)
    logger.debug("Routers registered")

    return app


def register_extensions(app: FastAPI) -> None:
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cors.init_app(app, supports_credentials=True)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    return None


def register_routers(app: FastAPI) -> None:
    """Register Flask blueprints."""
    # app.register_blueprint(user_bp)
    app.include_router(status_route, prefix="/v1/status", tags=["status"])
    # app.register_blueprint(configurator_bp)
    # app.register_blueprint(data_bp)
    # app.register_blueprint(mine_bp)
    # app.register_blueprint(build_bp)
    return None
