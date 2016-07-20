#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getpass
import click
from datetime import datetime

from .run import app
from .extensions import db
from .account.models import create_user, Permission
from .permissions import Need
from .setting.models import init_settings

import feedparser
from .post.models import Post
from .tag.models import Tag


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
    # path = raw_input('path: ')
    path = 'wordpress.2016-07-07.xml'
    feed = feedparser.parse(path)
    for entry in feed.entries:
        # print entry.keys()
        post = Post()
        post.title = entry.title
        # print entry.content
        post.content = entry.content[0]['value']
        for tag_dict in entry.tags:
            tag = Tag.query.filter_by(name=tag_dict['term']).first()
            if not tag:
                tag = Tag(name=tag_dict['term'])
            post.tags.append(tag)

        published = datetime.strptime(entry.wp_post_date, '%Y-%m-%d %H:%M:%S')
        post.author_id = 1
        print published.strftime('%Y/%m/'+entry.wp_post_id)
        post.slug = published.strftime('%Y/%m/'+entry.wp_post_id)
        post.created_at = published
        post.updated_at = published
        db.session.add(post)
        db.session.commit()
    click.echo('over')


@app.cli.command()
def init():
    init_settings()
    click.echo('over')
