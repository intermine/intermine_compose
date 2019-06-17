from .users import user_bp

def init_app(app):
    app.register_blueprint(user_bp)