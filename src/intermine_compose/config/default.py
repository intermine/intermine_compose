"""App Config."""

from environs import Env
from pydantic import BaseSettings

# Read env variables from a .env file
env = Env()
env.read_env()

HOME = env.str("HOME")
APP_HOST = env.str("APP_PORT", default="localhost")
APP_PORT = env.str("APP_PORT", default="9991")
APP_DEBUG = env.bool("APP_DEBUG", default=False)
ENV = env.str("APP_ENV", default="development")
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", default="redis")
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default="redis://127.0.0.1:6379")
KUBERNETES_CONFIG_PATH = env.str(
    "KUBERNETES_CONFIG_PATH", default=f"{HOME}/.kube/config"
)
SQLALCHEMY_TRACK_MODIFICATIONS = env.bool(
    "SQLALCHEMY_TRACK_MODIFICATIONS", default=False
)
SQLALCHEMY_DATABASE_URI = env.str(
    "SQLALCHEMY_DATABASE_URI",
    default="postgresql://postgres:postgres@localhost:5432/compose",
)
SECRET_KEY = env.str("SECRET_KEY", default="ADD_A_RANDOM_KEY_HERE")
SENDGRID_API_KEY = env.str("SENDGRID_API_KEY", default="GIVE_ME_SENDGRID_KEY")
MAIL_SUPPRESS_SEND = env.bool("MAIL_SUPPRESS_SEND", default=True)
FRONTEND_DOMAIN_NAME = env.str("FRONTEND_DOMAIN_NAME", default="example.com")
DEFAULT_EMAIL_ORIGIN = env.str("DEFAULT_EMAIL_ORIGIN", default="admin@exampmle.com")


class DefaultConfig(BaseSettings):
    """Default config class."""

    HOME = env.str("HOME")
    APP_NAME: str = "compose"
    APP_HOST: str = "localhost"
    APP_PORT: int = 9991
    APP_ENV: str = "development"
    APP_DEBUG: bool = False
    APP_LOG: str = "info"
    ALGORITHM = "HS256"
    APP_SECRET = "SECERT_KEY"
    API_KEY = "SECRET_KEY"
    API_KEY_NAME = "compose"
    COOKIE_DOMAIN = "localhost"
    ACCESS_TOKEN_EXPIRE_MINUTES = 1440
    CELERY_RESULT_BACKEND: str = "redis"
    CELERY_BROKER_URL: str = "redis://127.0.0.1:6379"
    KUBERNETES_CONFIG_PATH: str = f"{HOME}/.kube/config"
    # SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DB_NAME: str = "compose"
    DB_URI: str = "postgresql://postgres:postgres@localhost:5432/compose"
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    SECRET_KEY: str = "ADD_A_RANDOM_KEY_HERE"
    SENDGRID_API_KEY: str = "GIVE_ME_SENDGRID_KEY"
    MAIL_SUPPRESS_SEND: bool = False
    FRONTEND_DOMAIN_NAME: str = "example.com"
    DEFAULT_EMAIL_ORIGIN: str = "admin@exampmle.com"
