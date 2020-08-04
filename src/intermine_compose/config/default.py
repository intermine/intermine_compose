"""App Config."""

import os

from environs import Env

# Read env variables from a .env file
env = Env()
env.read_env()

HOME = env.str("HOME")
FLASK_HOST = env.str("FLASK_PORT", default="localhost")
FLASK_PORT = env.str("FLASK_PORT", default="9991")
FLASK_DEBUG = env.bool("FLASK_DEBUG", default=False)
ENV = env.str("FLASK_ENV", default="development")
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
