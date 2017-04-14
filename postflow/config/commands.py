# -*- coding: utf-8 -*-

import os
import sys
import click
from flask import current_app
from werkzeug.security import gen_salt
from jinja2 import Environment, FileSystemLoader

from postflow.commands.base import postflow


@postflow.group()
def config():
    """Create, update or delete theme."""
    pass

def prompt_config_path(config_path):
    """Asks for a config path. If the path exists it will ask the user
    for a new path until a he enters a path that doesn't exist.

    :param config_path: The path to the configuration.
    """
    click.secho("The path to save this configuration file.", fg="cyan")
    while True:
        if os.path.exists(config_path) and click.confirm(click.style(
            "Config {cfg} exists. Do you want to overwrite it?"
            .format(cfg=config_path), fg="magenta")):
            break

        config_path = click.prompt(
            click.style("Save to", fg="magenta"),
            default=config_path)

        if not os.path.exists(config_path):
            break

    return config_path


def write_config(config, config_template, config_path):
    """Writes a new config file based upon the config template.

    :param config: A dict containing all the key/value pairs which should be
                   used for the new configuration file.
    :param config_template: The config (jinja2-)template.
    :param config_path: The place to write the new config file.
    """
    with open(config_path, 'w') as cfg_file:
        cfg_file.write(
            config_template.render(**config).encode("utf-8")
        )

def generate_config(output=None, force=None, theme=None):
    config_env = Environment(
        loader=FileSystemLoader(os.path.join(current_app.root_path, "config"))
    )
    config_template = config_env.get_template('config.conf.tpl')

    if output:
        config_path = os.path.abspath(output)
    else:
        config_path = current_app.instance_path

    if os.path.exists(config_path) and not os.path.isfile(config_path):
        config_path = os.path.join(config_path, "postflow.conf")

    default_conf = {
        "secret_key": gen_salt(24),
        "database_uri": "sqlite:///" + os.path.join(current_app.instance_path, "content/data/postflow.db"),
        "theme_paths": "content/themes",
        "theme": theme or 'casper',
        "mail_server": "localhost",
        "mail_port": 25,
        "mail_use_tls": False,
        "mail_use_ssl": False,
        "mail_username": "",
        "mail_password": "",
        "mail_sender_name": "PostFlow Mailer",
        "mail_sender_address": "noreply@yourdomain",
        "mail_admin_address": "admin@yourdomain",
        'storage_type': 'local',
        'storage_base_url': '/',
        'storage_base_path': current_app.instance_path,
        'storage_base_dir': 'content/images/',
    }

    if not force:
        config_path = prompt_config_path(config_path)

    if force and os.path.exists(config_path):
        click.secho("Overwriting existing config file: {}".format(config_path),
                    fg="yellow")

    write_config(default_conf, config_template, config_path)

    return config_path


@config.command("generate")
@click.option("--output", "-o", required=False,
              help="The path where the config file will be saved at. "
                   "Defaults to the PostFlow's root folder.")
@click.option("--force", "-f", default=False, is_flag=True,
              help="Overwrite any existing config file if one exists.")
def generate(output, force):
    """Generates a PostFlow configuration file."""
    config_path = generate_config(output, force)

    # Finished
    click.secho("The configuration file has been saved to:\n{cfg}"
                .format(cfg=config_path), fg="blue")
    click.secho("Usage: postflow --config {cfg} run\n"
                "Feel free to adjust it as needed."
                .format(cfg=config_path), fg="green")
    sys.exit(0)
