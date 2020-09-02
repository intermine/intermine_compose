"""Configs for app."""

from enum import Enum, unique
from functools import lru_cache
import os

from environs import Env
from logzero import logger

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
def get_config() -> DefaultConfig:
    """Cache and return config object."""
    if os.environ.get("APP_CONFIG", None) is not None:
        app_config = os.environ.get("APP_CONFIG")
    if os.environ.get("CI", None) is not None:
        app_config = "CI"
    else:
        env = Env()
        env.read_env()
        app_config = env.str("APP_CONFIG", "DEFAULT")
    logger.info(f"Config loaded: {app_config}")
    return Config[app_config].value()
