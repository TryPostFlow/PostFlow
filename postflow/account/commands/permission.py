# -*- coding: utf-8 -*-

import click

from postflow.commands import postflow
from postflow.account.commands.utils import init_permissions


@postflow.group()
def permissions():
    """Create, update or delete users."""
    pass


@permissions.command("init")
def init():
    """Creates a new user. Omit any options to use the interactive mode."""
    click.secho("[+] Initialize permissions", fg="cyan")
    init_permissions()
    click.secho("[+] Initialize permissions successfully", fg="green")
