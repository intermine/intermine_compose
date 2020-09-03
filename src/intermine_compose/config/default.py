"""App Config."""

from pydantic import BaseSettings


class DefaultConfig(BaseSettings):
    """Default config class."""

    HOME: str
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
    COOKIE_SECURE = True
    COOKIE_SAMESITE = "lax"
    ACCESS_TOKEN_EXPIRE_MINUTES = 1440
    CELERY_RESULT_BACKEND: str = "redis"
    CELERY_BROKER_URL: str = "redis://127.0.0.1:6379"
    # KUBERNETES_CONFIG_PATH: str = f"{HOME}/.kube/config"
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
