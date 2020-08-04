from intermine_compose.config.default import env

SQLALCHEMY_DATABASE_URI = env.str(
    "SQLALCHEMY_DATABASE_URI",
    default="postgresql://postgres:postgres@postgres:5432/compose",
)
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default="redis://redis:6379")
FLASK_DEBUG = env.bool("FLASK_DEBUG", default=True)
