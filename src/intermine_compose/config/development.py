"""App Config."""

from intermine_compose.config.default import env

SQLALCHEMY_ECHO = env.bool("SQLALCHEMY_ECHO", default=True)
FLASK_DEBUG = env.bool("FLASK_DEBUG", default=True)
