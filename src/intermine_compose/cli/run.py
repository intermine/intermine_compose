"""Run command."""

import click

from intermine_compose.app import create_app
from intermine_compose.config import Config


@click.command()
@click.option("-c", "--config", help="Set config to load")
def run(config: str) -> None:
    """Run command."""
    click.secho("Staring App!", fg="green")
    if config:
        try:
            app = create_app(Config[config])
        except:
            app = create_app()
    else:
        app = create_app()

    app.run(
        host=app.config.get("FLASK_HOST"),
        port=app.config.get("FLASK_PORT"),
        debug=app.config.get("FLASK_DEBUG"),
    )
