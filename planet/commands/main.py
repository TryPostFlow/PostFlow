#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pkgutil
import getpass
import click
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from werkzeug.security import gen_salt
from flask import current_app
from flask.cli import FlaskGroup, ScriptInfo, pass_script_info, with_appcontext
from sqlalchemy_utils.functions import (database_exists, drop_database)

from planet import create_app
from planet._compat import iteritems
from planet.extensions import db, alembic
from planet.setting.models import init_settings

import feedparser
from planet.post.models import Post
from planet.tag.models import Tag
from planet.oauth.models import create_client
from planet.commands.utils import (FlaskCLIError, create_permissions,
                                   EmailType, prompt_save_user, prompt_config_path,
                                   write_config)


def make_app(script_info):
    config_file = getattr(script_info, "config_file")
    return create_app(config_file)


def set_config(ctx, param, value):
    """This will pass the config file to the create_app function."""
    ctx.ensure_object(ScriptInfo).config_file = value


@click.group(cls=FlaskGroup, create_app=make_app, add_version_option=False)
@click.option('--config', default="planet.conf", expose_value=False, callback=set_config,
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
@click.option("--role", "-r", help="The role of the user.",
              type=click.Choice(["admin", "super_mod", "mod", "member"]))
def install(force, username, email, password, role):
    """Installs planet. If no arguments are used, an interactive setup
    will be run.
    """
    click.secho("[+] Installing Planet...", fg="cyan")
    if database_exists(db.engine.url):
        if force or click.confirm(click.style(
            "Existing database found. Do you want to delete the old one and "
            "create a new one?", fg="magenta")):
            drop_database(db.engine.url)
        else:
            sys.exit(0)
    # create_database(db.engine.url)
    db.create_all()
    alembic.upgrade()
    click.secho("[+] Creating default settings...", fg="cyan")
    create_client('planet')
    create_permissions()
    init_settings()

    click.secho("[+] Creating admin user...", fg="cyan")
    prompt_save_user(username, email, password, role)

    click.secho("[+] FlaskBB has been successfully installed!",
                fg="green", bold=True)


@planet.command("shell", short_help="Runs a shell in the app context.")
@with_appcontext
def shell_command():
    """Runs an interactive Python shell in the context of a given
    Flask application.  The application will populate the default
    namespace of this shell according to it"s configuration.
    This is useful for executing small snippets of management code
    without having to manually configuring the application.

    This code snippet is taken from Flask"s cli module and modified to
    run IPython and falls back to the normal shell if IPython is not
    available.
    """
    import code
    banner = "Python %s on %s\nInstance Path: %s" % (
        sys.version,
        sys.platform,
        current_app.instance_path,
    )
    ctx = {"db": db}

    # Support the regular Python interpreter startup script if someone
    # is using it.
    startup = os.environ.get("PYTHONSTARTUP")
    if startup and os.path.isfile(startup):
        with open(startup, "r") as f:
            eval(compile(f.read(), startup, "exec"), ctx)

    ctx.update(current_app.make_shell_context())

    try:
        import IPython
        IPython.embed(banner1=banner, user_ns=ctx)
    except ImportError:
        code.interact(banner=banner, local=ctx)


@planet.command("makeconfig")
@click.option("--development", "-d", default=False, is_flag=True,
              help="Creates a development config with DEBUG set to True.")
@click.option("--output", "-o", required=False,
              help="The path where the config file will be saved at. "
                   "Defaults to the flaskbb's root folder.")
@click.option("--force", "-f", default=False, is_flag=True,
              help="Overwrite any existing config file if one exists.")
def generate_config(development, output, force):
    """Generates a Planet configuration file."""
    config_env = Environment(
        loader=FileSystemLoader(os.path.join(current_app.root_path, "configs"))
    )
    config_template = config_env.get_template('config.conf.tpl')

    if output:
        config_path = os.path.abspath(output)
    else:
        config_path = current_app.instance_path

    if os.path.exists(config_path) and not os.path.isfile(config_path):
        config_path = os.path.join(config_path, "planet.conf")

    default_conf = {
        "debug": True,
        "server_name": "localhost:5000",
        "secret_key": gen_salt(24),
        "database_uri": "sqlite:///" + os.path.join(current_app.instance_path, "content/data/planet.db"),
        "theme_paths": "content/themes",
        "mail_server": "localhost",
        "mail_port": 25,
        "mail_use_tls": False,
        "mail_use_ssl": False,
        "mail_username": "",
        "mail_password": "",
        "mail_sender_name": "Planet Mailer",
        "mail_sender_address": "noreply@yourdomain",
        "mail_admin_address": "admin@yourdomain",
        'storage_type': 'local',
        'storage_base_url': 'localhost:5000',
        'storage_base_path': current_app.instance_path,
        'storage_base_dir': 'content/images/',
    }

    if not force:
        config_path = prompt_config_path(config_path)

    if force and os.path.exists(config_path):
        click.secho("Overwriting existing config file: {}".format(config_path),
                    fg="yellow")

    # if development:
    write_config(default_conf, config_template, config_path)

    # Finished
    click.secho("The configuration file has been saved to:\n{cfg}"
                .format(cfg=config_path), fg="blue")
    click.secho("Usage: planet --config {cfg} run\n"
                "Feel free to adjust it as needed."
                .format(cfg=config_path), fg="green")
    sys.exit(0)


@planet.command()
@click.option("--path", "-p",
              help="The configuration file to use for FlaskBB.")
def import_wordpress(path):
    feed = feedparser.parse(path)
    for entry in feed.entries:
        post = Post()
        post.title = entry.title
        post.content = entry.content[0]['value']
        for tag_dict in entry.tags:
            tag = Tag.query.filter_by(name=tag_dict['term']).first()
            if not tag:
                tag = Tag(name=tag_dict['term'])
            post.tags.append(tag)

        published = datetime.strptime(entry.wp_post_date, '%Y-%m-%d %H:%M:%S')
        post.created_by = 1
        post.updated_by = 1
        post.published_by = 1
        post.slug = published.strftime('%Y/%m/'+entry.wp_post_id)
        post.created_at = published
        post.updated_at = published
        post.updated_at = published
        db.session.add(post)
        db.session.commit()
        click.secho("[+] {} created.".format(post.title), fg="cyan")
    click.secho("[+] The file has been successfully imported!",
                fg="green", bold=True)
