# -*- coding: utf-8 -*-

import click

from planet.extensions import db
from planet.commands import planet


@planet.group()
def database():
    """Create, update or delete users."""
    pass


@database.command("create")
def createdb():
    """Initialize the database."""
    click.echo('creat the db')
    db.create_all()
    click.echo('over')


@database.command("drop")
def dropdb():
    """Initialize the database."""
    click.echo('drop the db')
    db.drop_all()
    click.echo('over')
