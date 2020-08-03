from flask import Flask
from logzero import logger

from intermine_compose.config import Config
from intermine_compose.extentions import bcrypt, cors, db, login_manager, migrate
from intermine_compose.routes import (
    build_bp,
    configurator_bp,
    data_bp,
    status_bp,
    mine_bp,
    user_bp,
)

import os


def create_app(config: Config) -> Flask:
    app = Flask(__name__, template_folder="./templates")
    logger.info("App instance created")

    # Loads default config defined in config dir
    app.config.from_object("intermine_compose.config.default")

    # Loads specific config defined in config dir
    app.config.from_object(f"intermine_compose.config.{config.value}")
    logger.debug(f"Config loaded: {config.value}")

    # Register app extentions
    register_extensions(app)
    logger.debug("Extensions loaded")

    # register blueprints
    register_blueprints(app)
    logger.debug("Blueprints registered")

    return app


def register_extensions(app: Flask) -> None:
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cors.init_app(app, supports_credentials=True)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app: Flask) -> None:
    """Register Flask blueprints."""
    app.register_blueprint(user_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(configurator_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(mine_bp)
    app.register_blueprint(build_bp)
    return None
