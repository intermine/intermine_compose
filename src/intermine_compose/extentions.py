"""App extenstions."""

from environs import Env
from flask_bcrypt import Bcrypt  # type: ignore
from flask_cors import CORS
from flask_login import LoginManager  # type: ignore
from flask_migrate import Migrate  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
import marshmallow
from sendgrid import SendGridAPIClient

bcrypt = Bcrypt()
cors = CORS()
login_manager = LoginManager()
db: SQLAlchemy = SQLAlchemy()
migrate = Migrate()
ma = marshmallow

env = Env()
env.read_env()
