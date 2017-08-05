#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click

from postflow.commands import postflow
from postflow.setting.fixtures import init_settings



@postflow.group()
def settings():
    """Create, update or delete users."""
    pass

@settings.command("init")
def init():
    click.secho("[+] Initialize settings", fg="cyan")
    init_settings()
    click.secho("[+] Initialize settings successfully", fg="green")
