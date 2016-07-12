#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getpass
import click

from .run import app
from .extensions import db
from .account.models import create_user, Permission
from .permissions import Need

import feedparser


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
        permission = Permission.query.filter(
            Permission.object_type == need.method,
            Permission.action_type == need.value).first()
        if not permission:
            db.session.add(
                Permission(
                    object_type=need.method,
                    action_type=need.value))
    db.session.commit()
    click.echo('over')


@app.cli.command()
def import_wordpress():
    path = raw_input('path: ')
    feed = feedparser.parse(path)
    print feed.feed.title
    print feed.entries[0].wp_post_id
