# -*- coding: utf-8 -*-

import sys
import click

from sqlalchemy_utils.functions import (database_exists, drop_database)

from postflow.extensions import db as sqlalchemy
from postflow.extensions import alembic
from postflow.commands.base import postflow


@postflow.group()
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

def init_db(force):
    if database_exists(sqlalchemy.engine.url):
        if force or click.confirm(click.style(
            "Existing database found. Do you want to delete the old one and "
            "create a new one?", fg="magenta")):
            drop_database(sqlalchemy.engine.url)
        else:
            return
    # create_database(db.engine.url)
    sqlalchemy.create_all()
    alembic.upgrade()

@db.command("init")
@click.option("--force", "-f", default=False, is_flag=True,
              help="Doesn't ask for confirmation.")
def init(force):
    init_db(force)
    click.secho("[+] Database has been successfully initialized!",
                fg="green", bold=True)
