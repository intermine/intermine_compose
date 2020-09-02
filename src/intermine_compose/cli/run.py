"""Run command."""

import click
import uvicorn

from intermine_compose.app import create_app
from intermine_compose.extentions import settings


@click.command()
def run() -> None:
    """Run command."""
    click.secho("Staring App!", fg="green")
    app = create_app()
    uvicorn.run(
        app, host=settings.APP_HOST, port=settings.APP_PORT, log_level=settings.APP_LOG,
    )
