"""db command."""

import click

from intermine_compose.database import db as _db, destroy_db, init_db, reset_db


@click.command()
def init() -> None:
    """Init database."""
    click.secho("Creating database!", fg="green")
    init_db(_db)


@click.command()
def destroy() -> None:
    """Destroy database."""
    click.secho("Destroying database!", fg="red")
    destroy_db(_db)


@click.command()
def reset() -> None:
    """Reset database."""
    click.secho("Resetting database!", fg="yellow")
    reset_db(_db)


@click.group()
def db() -> None:
    """Database commands."""
    pass


db.add_command(init)
db.add_command(destroy)
db.add_command(reset)
