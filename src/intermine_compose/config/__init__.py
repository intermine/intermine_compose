"""Configs for app."""

from enum import Enum, unique

from . import default  # noqa


@unique
class Config(Enum):
    """Config enum."""

    CI = "testing_ci"
    DEFAULT = "default"
    DEV = "development"
    DOCKER_DEV = "docker_dev"
    PROD = "production"
    TEST = "testing"
