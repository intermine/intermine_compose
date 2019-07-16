from .users import user_bp
from .status import status_bp

def init_app(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(status_bp)
