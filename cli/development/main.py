# -*- coding: utf-8 -*-
import click
from sqlalchemy import inspect, make_url
from sqlalchemy_utils import database_exists, drop_database

from omdb.config import config
from omdb.db.base import db


@click.group(name='dev')
def subcommands():
    """
    Run development servers and services
    """


@click.command()
@click.option('--host', default='0.0.0.0')  # nosec  # noqa: S104
@click.option('--port', default=5555, type=int)
@click.option('--debug', default=True, type=bool)
@click.pass_context
def server(context, host: str, port: int, debug: bool):
    """Run the Flask dev server."""

    context.obj.app.run(host=host, port=port, debug=debug)


@click.command()
@click.option('--remove_all', default=False, type=bool)
@click.pass_context
def clean_db(context, remove_all: bool):
    """Clean up databases"""

    if not config.is_development():
        raise click.ClickException('This command is only available in development mode.')

    with context.obj.app.app_context():
        _inspect = inspect(db.engine)
        for db_name in _inspect.get_schema_names():
            if not remove_all and not db_name.startswith('test'):
                click.secho(f'Skipping database: {db_name}', fg='yellow')
                continue

            db_url = make_url(config.SQLALCHEMY_DATABASE_URI)
            db_url = db_url.set(database=f'{db_name}')
            db_uri = db_url.render_as_string(hide_password=False)
            if database_exists(db_uri):
                click.secho(f'Dropping database: {db_name}', fg='red', bold=True)
                drop_database(db_uri)


subcommands.add_command(server)
subcommands.add_command(clean_db)
