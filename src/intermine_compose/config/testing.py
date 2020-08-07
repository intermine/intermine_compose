"""Test Config."""

from intermine_compose.config.default import DefaultConfig


class TestConfig(DefaultConfig):
    """Test config."""

    DATABASE_URI: str = "postgresql://postgres:postgres@localhost:5432/compose_test"
    DB_NAME: str = "compose_test"
    APP_DEBUG: bool = True
    APP_LOG: str = "debug"
    ENV: str = "testing"
    MAIL_SUPPRESS_SEND: bool = True
