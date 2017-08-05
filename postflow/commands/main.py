#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pkgutil

import click
from flask import current_app
from flask.cli import with_appcontext

from postflow import create_app
from postflow._compat import iteritems
from postflow.extensions import db
from postflow.commands.utils import (FlaskCLIError, create_permissions,
                                   EmailType, prompt_save_user)
from postflow.commands.base import postflow
from postflow.commands.database import init_db
from postflow.commands.theme import download_theme
from postflow.config.commands import generate_config
from postflow.setting.fixtures import init_settings
from postflow.setting.models import save_setting
from postflow.oauth.models import Client
from postflow.account.commands.utils import init_permissions
from postflow.post.commands import insert_sample_post


@postflow.command()
@click.option(
    "--server",
    "-s",
    default="gunicorn",
    type=click.Choice(["gunicorn", "gevent"]),
    help="The WSGI Server to run PostFlow on.")
@click.option(
    "--host",
    "-h",
    default="127.0.0.1",
    help="The interface to bind PostFlow to.")
@click.option(
    "--port",
    "-p",
    default="8000",
    type=int,
    help="The port to bind PostFlow to.")
@click.option(
    "--workers",
    "-w",
    default=4,
    help="The number of worker processes for handling requests.")
@click.option(
    "--daemon",
    "-d",
    default=False,
    is_flag=True,
    help="Starts gunicorn as daemon.")
@click.option(
    "--config", "-c", help="The configuration file to use for PostFlow.")
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
                    config = dict(
                        [(key, value)
                         for key, value in iteritems(self.options)
                         if key in self.cfg.settings and value is not None])
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
            raise FlaskCLIError(
                "Cannot import gunicorn. "
                "Make sure it is installed.",
                fg="red")
    elif server == "gevent":
        try:
            from gevent import __version__
            from gevent.pywsgi import WSGIServer
            click.secho("* Starting gevent {}".format(__version__))
            click.secho("* Listening on http://{}:{}/".format(host, port))
            http_server = WSGIServer((host, port), create_app(config=config))
            http_server.serve_forever()
        except ImportError:
            raise FlaskCLIError(
                "Cannot import gevent. "
                "Make sure it is installed.",
                fg="red")


def prepare_folder(path):
    # Todo: change permission
    folder = os.path.join(current_app.instance_path, path)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    return folder


@postflow.command()
@click.option(
    "--force",
    "-f",
    default=False,
    is_flag=True,
    help="Doesn't ask for confirmation.")
@click.option("--name", "-u", help="The name of the user.")
@click.option(
    "--email", "-e", type=EmailType(), help="The email address of the user.")
@click.option("--password", "-p", help="The password of the user.")
def init(force, name, email, password):
    """Installs postflow. If no arguments are used, an interactive setup
    will be run.
    """
    click.secho("[+] Installing PostFlow...", fg="cyan")
    # Prepare Content folder
    click.secho("[+] Prepareing content folder...", fg="cyan")
    data_folder = prepare_folder('content/data/')
    images_folder = prepare_folder('content/images/')
    themes_folder = prepare_folder('content/themes/')
    click.secho("[+] Content folder is ready.", fg="green")

    # # Create admin user
    click.secho("[+] Creating admin user...", fg="cyan")
    if not name:
        name = click.prompt(
            click.style("Name", fg="magenta"),
            type=str,
            default=os.environ.get("USER", ""))
    if not email:
        email = click.prompt(
            click.style("Email address", fg="magenta"), type=EmailType())
    if not password:
        password = click.prompt(
            click.style("Password", fg="magenta"),
            hide_input=True,
            confirmation_prompt=True)

    # Create Site
    click.secho("[+] Creating site...", fg="cyan")
    site_name = click.prompt(
        click.style("Site name", fg="magenta"), type=str, default="PostFlow")

    # Select Theme
    click.secho("[+] Installing theme...", fg="cyan")
    # path = click.prompt(
    #     click.style("Theme name (Github: user_name/repo_name)", fg="magenta"), type=str,
    #     default="fengluo/casper")
    # download theme
    theme_name = download_theme("fengluo/casper")
    click.secho("[+] Theme is ready.", fg="green")

    # generate config
    click.secho("[+] Generating config...", fg="cyan")
    config_path = generate_config(theme=theme_name)
    click.secho(
        "The configuration file has been saved to:\n{cfg}".format(
            cfg=config_path),
        fg="blue")
    current_app.config.from_pyfile(config_path)
    click.secho("[+] Config is ready.", fg="green")

    # init database
    click.secho("[+] Initializing database...", fg="cyan")
    init_db(force)
    click.secho("[+] Database is ready.", fg="green")

    # Insert data
    click.secho("[+] Insert data...", fg="cyan")
    Client.create(name='postflow')
    init_permissions()
    init_settings()
    save_setting('title', site_name)
    prompt_save_user(name, email, password, 'owner')
    insert_sample_post()
    click.secho("[+] Data is ready.", fg="green")

    click.secho(
        "[+] PostFlow has been successfully initialized!", fg="green", bold=True)


@postflow.command("shell", short_help="Runs a shell in the app context.")
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
        sys.version, sys.platform, current_app.instance_path, )
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
