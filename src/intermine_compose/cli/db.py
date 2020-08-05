"""db command."""

import click
from environs import Env

from intermine_compose.app import create_app
from intermine_compose.config import Config
from intermine_compose.extentions import db as _db


@click.command()
@click.option("-c", "--config", help="Set config to load")
def init(config: str) -> None:
    """Init database."""
    click.secho("Creating database!", fg="green")
    env = Env()
    env.read_env()
    if config:
        try:
            app = create_app(Config[config])
        except BaseException:
            app = create_app()
    else:
        if env.bool("CI", default=False):
            app = create_app(Config.CI)
        else:
            app = create_app()
    _db.init_app(app)
    with app.app_context():
        _db.create_all()


@click.command()
@click.option("-c", "--config", help="Set config to load")
def destroy(config: str) -> None:
    """Destroy database."""
    click.secho("Destroying database!", fg="red")
    env = Env()
    env.read_env()
    if config:
        try:
            app = create_app(Config[config])
        except BaseException:
            app = create_app()
    else:
        if env.bool("CI", default=False):
            app = create_app(Config.CI)
        else:
            app = create_app()
    _db.init_app(app)
    with app.app_context():
        _db.session.close()
        _db.drop_all()


@click.command()
@click.option("-c", "--config", help="Set config to load")
def reset(config: str) -> None:
    """Reset database."""
    click.secho("Resetting database!", fg="yellow")
    env = Env()
    env.read_env()
    if config:
        try:
            app = create_app(Config[config])
        except BaseException:
            app = create_app()
    else:
        if env.bool("CI", default=False):
            app = create_app(Config.CI)
        else:
            app = create_app()
    _db.init_app(app)
    with app.app_context():
        _db.session.close()
        _db.drop_all()
        _db.create_all()
        _db.session.close()


@click.group()
def db() -> None:
    """Database commands."""
    pass


db.add_command(init)
db.add_command(destroy)
db.add_command(reset)
