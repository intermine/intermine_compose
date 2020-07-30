"""Configs for app."""

from enum import Enum, unique

from . import default  # noqa


@unique
class Config(Enum):
    """Config enum."""

    DEFAULT = "default"
    DEV = "development"
    DOCKER = "docker"
    TEST = "testing"
    CI = "testing_ci"
