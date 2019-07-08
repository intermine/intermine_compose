import os

HOME = os.environ.get("HOME")
CELERY_RESULT_BACKEND = "redis"
CELERY_BROKER_URL = "redis://127.0.0.1:6379"
KUBERNETES_CONFIG_PATH = f"{HOME}/.kube/config"
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
SQLALCHEMY_DATABASE_URI = "postgres://postgres:postgres@localhost:5432/composedb"
SQLALCHEMY_ECHO = True
DEV_DB = True