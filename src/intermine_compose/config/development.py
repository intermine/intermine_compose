"""App Config."""

from intermine_compose.config.default import DefaultConfig


class DevConfig(DefaultConfig):
    """Dev config."""

    APP_DEBUG: bool = True
    APP_LOG: str = "debug"
