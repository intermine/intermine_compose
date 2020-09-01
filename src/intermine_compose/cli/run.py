"""Run command."""

import os

import click
from logzero import logger
import uvicorn

from intermine_compose.app import create_app
from intermine_compose.extentions import settings


@click.command()
@click.option("-c", "--config", help="Set config to load")
def run(config: str) -> None:
    """Run command."""
    click.secho("Staring App!", fg="green")
    if config:
        os.environ["APP_CONFIG"] = config
        logger.info(f"Setting APP_CONFIG: {config}")

    app = create_app()

    uvicorn.run(
        app, host=settings.APP_HOST, port=settings.APP_PORT, log_level=settings.APP_LOG,
    )
