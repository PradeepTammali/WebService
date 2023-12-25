# -*- coding: utf-8 -*-
import click


@click.group(name='dev')
def subcommands():
    """
    Run development servers and services
    """


@click.command()
@click.option('--host', default='0.0.0.0')  # nosec  # noqa: S104
@click.option('--port', default=6000, type=int)
@click.option('--debug', default=True, type=bool)
@click.pass_context
def server(context, host: str, port: int, debug: bool):
    """Run the Flask dev server."""

    context.obj.app.run(host=host, port=port, debug=debug)


subcommands.add_command(server)
