# -*- coding: utf-8 -*-

import click

from planet.extensions import db as sqlalchemy
from planet.commands import planet


@planet.group()
def db():
    """Create, update or delete users."""
    pass


@db.command("create")
def createdb():
    """Initialize the database."""
    click.echo('creat the db')
    sqlalchemy.create_all()
    click.echo('over')


@db.command("drop")
def dropdb():
    """Initialize the database."""
    click.echo('drop the db')
    sqlalchemy.drop_all()
    click.echo('over')
