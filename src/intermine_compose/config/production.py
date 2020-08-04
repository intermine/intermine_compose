from intermine_compose.config.default import env

FLASK_DEBUG = env.bool("FLASK_DEBUG", default=False)
ENV = env.str("FLASK_ENV", default="production")
FLASK_HOST = env.str("FLASK_HOST", default="0.0.0.0")
FLASK_PORT = env.str("FLASK_PORT", default="9991")
MAIL_SERVER = env.str("MAIL_SERVER")
MAIL_PORT = env.str("MAIL_PORT")
MAIL_USE_TLS = env.str("MAIL_USE_TLS")
MAIL_USE_SSL = env.str("MAIL_USE_SSL")
MAIL_USERNAME = env.str("MAIL_USERNAME")
MAIL_PASSWORD = env.str("MAIL_PASSWORD")
