from .logger import custom_logger
def init_app(app):
    custom_logger.init_app(app)