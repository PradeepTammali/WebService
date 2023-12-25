# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position,import-outside-toplevel
import sys
from pathlib import Path

import click

sys.path.append(Path(__file__).resolve().parent.parent.as_posix())


from cli.development.main import subcommands as development_group  # noqa: E402


class App:
    _app = None

    @property
    def app(self):
        if self._app is None:
            from run import app  # noqa: E402

            self._app = app

        return self._app


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.pass_context
def cli(context):
    """
    Type 'omdb <subcommand> -h' for help on a specific subcommand.
    """
    context.obj = App()


cli.add_command(development_group)
