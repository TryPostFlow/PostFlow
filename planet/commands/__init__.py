#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pkgutil
import getpass
import click
from datetime import datetime
from flask.cli import FlaskGroup, ScriptInfo, pass_script_info
from sqlalchemy_utils.functions import (database_exists, create_database,
                                        drop_database)

from planet import create_app
from planet.run import app
from planet._compat import iteritems
from planet.extensions import db, alembic
from planet.setting.models import init_settings

import feedparser
from planet.post.models import Post
from planet.tag.models import Tag

from planet.commands.utils import (FlaskCLIError, create_permissions, EmailType, prompt_save_user)


def make_app(script_info):
    config_file = getattr(script_info, "config_file")
    return create_app(config_file)


def set_config(ctx, param, value):
    """This will pass the config file to the create_app function."""
    ctx.ensure_object(ScriptInfo).config_file = value


@click.group(cls=FlaskGroup, create_app=make_app, add_version_option=False)
@click.option('--config', expose_value=False, callback=set_config,
              required=False, is_flag=False, is_eager=True, metavar="CONFIG",
              help="Specify the config to use in dotted module notation "
                   "e.g. flaskbb.configs.default.DefaultConfig")
@pass_script_info
def planet(info, **params):
    os.environ["FLASK_DEBUG"] = str(info.load_app().config['DEBUG'])


@planet.command()
@click.option("--server", "-s", default="gunicorn",
              type=click.Choice(["gunicorn", "gevent"]),
              help="The WSGI Server to run FlaskBB on.")
@click.option("--host", "-h", default="127.0.0.1",
              help="The interface to bind FlaskBB to.")
@click.option("--port", "-p", default="8000", type=int,
              help="The port to bind FlaskBB to.")
@click.option("--workers", "-w", default=4,
              help="The number of worker processes for handling requests.")
@click.option("--daemon", "-d", default=False, is_flag=True,
              help="Starts gunicorn as daemon.")
@click.option("--config", "-c",
              help="The configuration file to use for FlaskBB.")
def start(server, host, port, workers, config, daemon):
    """Starts a production ready wsgi server.
    TODO: Figure out a way how to forward additional args to gunicorn
          without causing any errors.
    """
    if server == "gunicorn":
        try:
            from gunicorn.app.base import Application

            class FlaskApplication(Application):
                def __init__(self, app, options=None):
                    self.options = options or {}
                    self.application = app
                    super(FlaskApplication, self).__init__()

                def load_config(self):
                    config = dict([
                        (key, value) for key, value in iteritems(self.options)
                        if key in self.cfg.settings and value is not None
                    ])
                    for key, value in iteritems(config):
                        self.cfg.set(key.lower(), value)

                def load(self):
                    return self.application

            worker_class = 'sync'
            if pkgutil.find_loader('gevent'):
                worker_class = 'gunicorn.workers.ggevent.GeventWorker'

            options = {
                "bind": "{}:{}".format(host, port),
                "workers": workers,
                "daemon": daemon,
                "worker_class": worker_class
            }
            FlaskApplication(create_app(config=config), options).run()
        except ImportError:
            raise FlaskCLIError("Cannot import gunicorn. "
                                "Make sure it is installed.", fg="red")
    elif server == "gevent":
        try:
            from gevent import __version__
            from gevent.pywsgi import WSGIServer
            click.secho("* Starting gevent {}".format(__version__))
            click.secho("* Listening on http://{}:{}/".format(host, port))
            http_server = WSGIServer((host, port), create_app(config=config))
            http_server.serve_forever()
        except ImportError:
            raise FlaskCLIError("Cannot import gevent. "
                                "Make sure it is installed.", fg="red")


@planet.command()
@click.option("--force", "-f", default=False, is_flag=True,
              help="Doesn't ask for confirmation.")
@click.option("--username", "-u", help="The username of the user.")
@click.option("--email", "-e", type=EmailType(),
              help="The email address of the user.")
@click.option("--password", "-p", help="The password of the user.")
def install(force, username, email, password):
    """Installs planet. If no arguments are used, an interactive setup
    will be run.
    """
    click.secho("[+] Installing Planet...", fg="cyan")
    if database_exists(db.engine.url):
        if force or click.confirm(click.style(
            "Existing database found. Do you want to delete the old one and "
            "create a new one?", fg="magenta")
        ):
            drop_database(db.engine.url)
        else:
            sys.exit(0)
    # create_database(db.engine.url)
    db.create_all()
    # alembic.upgrade()
    click.secho("[+] Creating default settings...", fg="cyan")
    create_permissions()
    init_settings()

    click.secho("[+] Creating admin user...", fg="cyan")
    prompt_save_user(username, email, password, role)


@planet.command()
def createdb():
    """Initialize the database."""
    click.echo('creat the db')
    db.create_all()
    click.echo('over')


@app.cli.command()
def create_super_user():
    cmd = raw_input('Create superuser?(Y/n): ')
    if cmd == 'n':
        sys.exit(1)
    name = raw_input('name: ')
    email = raw_input('email: ')
    password = getpass.getpass('password: ')
    role = Role.query.filter_by(slug='admin').first()
    create_user(name=name,
                email=email,
                password=password,
                role=role)
    click.echo('over')


@app.cli.command()
def import_wordpress():
    # path = raw_input('path: ')
    path = 'wordpress.2016-07-07.xml'
    feed = feedparser.parse(path)
    for entry in feed.entries:
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
        post.created_by = 1
        post.updated_by = 1
        print published.strftime('%Y/%m/'+entry.wp_post_id)
        post.slug = published.strftime('%Y/%m/'+entry.wp_post_id)
        post.created_at = published
        post.updated_at = published
        db.session.add(post)
        db.session.commit()
    click.echo('over')
