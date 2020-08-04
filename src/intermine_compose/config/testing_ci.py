"""App Config."""

from intermine_compose.config.default import env

SQLALCHEMY_DATABASE_URI = env.str(
    "SQLALCHEMY_DATABASE_URI",
    default="postgresql://postgres:postgres@localhost:5432/compose_test",
)
SQLALCHEMY_ECHO = env.bool("SQLALCHEMY_ECHO", default=True)
MAIL_SUPPRESS_SEND = env.bool("MAIL_SUPPRESS_SEND", default=True)
ENV = env.str("FLASK_ENV", default="testing")
FLASK_DEBUG = env.bool("FLASK_DEBUG", default=True)
