from .user import user_bp
from .configurator import configurator_bp
from .status import status_bp
from .data import data_bp
from .mine import mine_bp
from .build import build_bp

def init_app(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(configurator_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(mine_bp)
    app.register_blueprint(build_bp)
