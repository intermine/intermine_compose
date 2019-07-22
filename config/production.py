import os

FLASK_DEBUG = False
FLASK_PORT = os.environ.get("PORT")
SQLALCHEMY_DATABASE_URI = f'postgres://{os.environ.get("PGUSER")}:{os.environ.get("PGPASSWORD")}@{os.environ.get("PGHOST")}:5432/composedb'
CELERY_BROKER_URL = f'redis://{os.environ.get("REDIS_PASSWORD")}@{os.environ.get("REDIS_HOST")}:6379'
SECRET_KEY = os.environ.get("SECRET_KEY")