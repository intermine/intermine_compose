"""db command."""

import os

import click
from logzero import logger

from intermine_compose.database import db as _db, destroy_db, init_db, reset_db


@click.command()
@click.option("-c", "--config", help="Set config to load")
def init(config: str) -> None:
    """Init database."""
    click.secho("Creating database!", fg="green")
    if config:
        os.environ["APP_CONFIG"] = config
        logger.info(f"Setting APP_CONFIG: {config}")
    init_db(_db)


@click.command()
@click.option("-c", "--config", help="Set config to load")
def destroy(config: str) -> None:
    """Destroy database."""
    click.secho("Destroying database!", fg="red")
    if config:
        os.environ["APP_CONFIG"] = config
        logger.info(f"Setting APP_CONFIG: {config}")
    destroy_db(_db)


@click.command()
@click.option("-c", "--config", help="Set config to load")
def reset(config: str) -> None:
    """Reset database."""
    click.secho("Resetting database!", fg="yellow")
    if config:
        os.environ["APP_CONFIG"] = config
        logger.info(f"Setting APP_CONFIG: {config}")
    reset_db(_db)


@click.group()
def db() -> None:
    """Database commands."""
    pass


db.add_command(init)
db.add_command(destroy)
db.add_command(reset)
