"""Command-line interface."""

import click

from intermine_compose.cli.db import db
from intermine_compose.cli.run import run
from .. import __version__


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Curation backend console."""


# main.add_command(hello)
main.add_command(run)
main.add_command(db)
