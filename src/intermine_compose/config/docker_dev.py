"""DockerDev Config."""

from intermine_compose.config.default import DefaultConfig


class DockerDevConfig(DefaultConfig):
    """DockerDev config."""

    DB_URI: str = "postgresql://postgres:postgres@postgres:5432/compose"
    DB_HOST: str = "postgres"
    CELERY_BROKER_URL: str = "redis://redis:6379"
    APP_DEBUG: bool = True
    APP_LOG: str = "debug"
