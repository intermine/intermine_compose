"""App extenstions."""

from environs import Env
from flask_bcrypt import Bcrypt  # type: ignore
from flask_cors import CORS
from flask_login import LoginManager  # type: ignore
from flask_migrate import Migrate  # type: ignore
from logzero import logger
import marshmallow
from sendgrid import SendGridAPIClient


from intermine_compose.config import Config, get_config

# initialize config
env = Env()
env.read_env()
app_config = env.str("APP_CONFIG", "DEFAULT")
logger.info(f"Config loaded: {app_config}")
settings = get_config(Config[app_config])

bcrypt = Bcrypt()
cors = CORS()
login_manager = LoginManager()

migrate = Migrate()
ma = marshmallow


sendGrid: SendGridAPIClient = SendGridAPIClient(
    api_key=env.str("SENDGRID_API_KEY", default="GIVE_ME_SENDGRID_KEY")
)
