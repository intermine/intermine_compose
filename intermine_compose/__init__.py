from flask import Flask
import os

def create_app():
    from . import models, routes, services
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.default')
    app.config.from_envvar('FLASK_CONFIG_FILE', silent=True)
    routes.init_app(app)
    services.init_app(app)
    models.init_app(app)
    app.app_context().push()
    if os.environ.get("DEV_DB"):
        models.drop_all_tables()
    models.create_all_tables()
    return app