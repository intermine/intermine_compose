from .base import login_manager

def init_app(app):
    login_manager.init_app(app)