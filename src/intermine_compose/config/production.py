import os

FLASK_DEBUG = False
FLASK_PORT = os.environ.get("PORT")
SQLALCHEMY_DATABASE_URI = f'postgres://{os.environ.get("PGUSER")}:{os.environ.get("PGPASSWORD")}@{os.environ.get("PGHOST")}:5432/composedb'
CELERY_BROKER_URL = f'redis://{os.environ.get("REDIS_PASSWORD")}@{os.environ.get("REDIS_HOST")}:6379'
SECRET_KEY = os.environ.get("SECRET_KEY")
MAIL_SERVER= os.environ.get("MAIL_SERVER")
MAIL_PORT=os.environ.get("MAIL_PORT")
MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
MAIL_USE_SSL=os.environ.get("MAIL_USE_SSL")
MAIL_USERNAME=os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")