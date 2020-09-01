"""Production config."""

from intermine_compose.config.default import DefaultConfig


class ProdConfig(DefaultConfig):
    """Production config."""

    APP_HOST: str = "0.0.0.0"
    APP_ENV: str = "production"
