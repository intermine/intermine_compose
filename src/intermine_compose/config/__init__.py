"""Configs for app."""

from enum import Enum, unique
from functools import lru_cache

from .default import DefaultConfig  # noqa
from .development import DevConfig
from .docker_dev import DockerDevConfig
from .production import ProdConfig
from .testing import TestConfig
from .testing_ci import TestCIConfig


@unique
class Config(Enum):
    """Config enum."""

    DEFAULT = DefaultConfig
    DEV = DevConfig
    DOCKER_DEV = DockerDevConfig
    PROD = ProdConfig
    TEST = TestConfig
    CI = TestCIConfig


@lru_cache()
def get_config(config: Config) -> DefaultConfig:
    """Cache and return config object."""
    return config.value()
