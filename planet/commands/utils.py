# -*- coding: utf-8 -*-

import os
import re
import click
from planet.extensions import db
from planet.utils.permissions import Need
from planet.account.models import (create_user, update_user, Permission, Role)


_email_regex = r"[^@]+@[^@]+\.[^@]+"


class FlaskCLIError(click.ClickException):
    """An exception that signals a usage error including color support.
    This aborts any further handling.

    :param styles: The style kwargs which should be forwarded to click.secho.
    """

    def __init__(self, message, **styles):
        click.ClickException.__init__(self, message)
        self.styles = styles

    def show(self, file=None):
        if file is None:
            file = click._compat.get_text_stderr()
        click.secho("[-] Error: %s" % self.format_message(), file=file,
                    **self.styles)


class EmailType(click.ParamType):
    """The choice type allows a value to be checked against a fixed set of
    supported values.  All of these values have to be strings.
    See :ref:`choice-opts` for an example.
    """
    name = "email"

    def convert(self, value, param, ctx):
        # Exact match
        if re.match(_email_regex, value):
            return value
        else:
            self.fail(("invalid email: %s" % value), param, ctx)

    def __repr__(self):
        return "email"


def create_permissions():
    admin = Role.query.filter_by(slug='admin').first()
    if not admin:
        admin = Role(name='Admin', slug='admin')
    for need in Need.needs:
        permission = Permission.query.filter(
            Permission.object_type == need.method,
            Permission.action_type == need.value).first()
        if not permission:
            permission = Permission(
                object_type=need.method,
                action_type=need.value)
            db.session.add(permission)
        admin.permissions.append(permission)
    db.session.add(admin)
    db.session.commit()


def prompt_save_user(name, email, password, role, only_update=False):
    if not name:
        name = click.prompt(
            click.style("Name", fg="magenta"), type=str,
            default=os.environ.get("USER", "")
        )
    if not email:
        email = click.prompt(
            click.style("Email address", fg="magenta"), type=EmailType()
        )
    if not password:
        password = click.prompt(
            click.style("Password", fg="magenta"), hide_input=True,
            confirmation_prompt=True
        )
    if not role:
        role = click.prompt(
            click.style("Role", fg="magenta"),
            type=click.Choice(["admin", "super_mod", "mod", "member"]),
            default="admin"
        )

    if only_update:
        return update_user(name, password, email, role)
    return create_user(name, password, email, role)


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
