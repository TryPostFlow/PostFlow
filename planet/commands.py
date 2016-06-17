#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getpass
import click

from .run import app
from .extensions import db
from .account.models import create_user, Permission
from .permissions import Need


@app.cli.command()
def createdb():
    """Initialize the database."""
    click.echo('creat the db')
    db.create_all()
    click.echo('over')


@app.cli.command()
def dropdb():
    """Initialize the database."""
    click.echo('drop the db')
    db.drop_all()
    click.echo('over')


@app.cli.command()
def create_super_user():
    cmd = raw_input('Create superuser?(Y/n): ')
    if cmd == 'n':
        sys.exit(1)
    name = raw_input('name: ')
    email = raw_input('email: ')
    password = getpass.getpass('password: ')
    create_user(name=name,
                email=email,
                password=password)
    click.echo('over')


@app.cli.command()
def register_actions():
    for need in Need._needs:
        db.session.add(
            Permission(object_type=need.method, action_type=need.value))
    db.session.commit()
    click.echo('over')
