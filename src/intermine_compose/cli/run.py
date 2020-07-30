"""Run command."""

import click

from intermine_compose.app import create_app
from intermine_compose.config import Config


@click.command()
def run() -> None:
    """Run command."""
    click.secho("Staring App!", fg="green")
    app = create_app(Config.DEFAULT)
    app.run(
        host=app.config.get("FLASK_HOST", "127.0.0.1"),
        port=app.config.get("FLASK_PORT", "9995"),
        debug=app.config.get("FLASK_DEBUG", True),
        load_dotenv=app.config.get("FLASK_LOAD_ENV", True),
    )
