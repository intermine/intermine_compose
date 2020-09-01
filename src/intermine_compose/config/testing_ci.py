"""App Config."""

from intermine_compose.config.default import DefaultConfig


class TestCIConfig(DefaultConfig):
    """Test config."""

    DATABASE_URI: str = "postgresql://postgres:postgres@localhost:5432/compose_test"
    DB_NAME: str = "compose"
    APP_DEBUG: bool = True
    APP_LOG: str = "debug"
    APP_ENV: str = "testing"
    MAIL_SUPPRESS_SEND: bool = True
