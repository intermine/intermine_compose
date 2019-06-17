from flask import Flask

def create_app():
    from . import models, routes, services
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.default')
    app.config.from_envvar('FLASK_CONFIG_FILE', silent=True)
    models.init_app(app)
    routes.init_app(app)
    services.init_app(app)
    return app