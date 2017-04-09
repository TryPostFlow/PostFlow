# -*- coding: utf-8 -*-

import click

from planet.commands import planet
from planet.account.commands.utils import init_permissions


@planet.group()
def permissions():
    """Create, update or delete users."""
    pass


@permissions.command("init")
def init():
    """Creates a new user. Omit any options to use the interactive mode."""
    click.secho("[+] Initialize permissions", fg="cyan")
    init_permissions()
    click.secho("[+] Initialize permissions successfully", fg="green")
