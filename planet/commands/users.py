# -*- coding: utf-8 -*-

import os
import sys
import click

from sqlalchemy.exc import IntegrityError
from planet.account.models import User
from planet.commands import planet
from planet.commands.utils import (EmailType, prompt_save_user, FlaskCLIError)


@planet.group()
def users():
    """Create, update or delete users."""
    pass


@users.command("new")
@click.option("--username", "-u", help="The username of the user.")
@click.option("--email", "-e", type=EmailType(),
              help="The email address of the user.")
@click.option("--password", "-p", help="The password of the user.")
@click.option("--role", "-r", help="The role of the user.",
              type=click.Choice(["admin", "super_mod", "mod", "member"]))
def new_user(username, email, password, role):
    """Creates a new user. Omit any options to use the interactive mode."""
    try:
        user = prompt_save_user(username, email, password, role)

        click.secho("[+] User {} with Email {} in Role {} created.".format(
            user.username, user.email, user.primary_group.name), fg="cyan")
    except IntegrityError:
        raise FlaskCLIError("Couldn't create the user because the "
                            "username or email address is already taken.",
                            fg="red")


@users.command("update")
@click.option("--username", "-u", help="The username of the user.")
@click.option("--email", "-e", type=EmailType(),
              help="The email address of the user.")
@click.option("--password", "-p", help="The password of the user.")
@click.option("--role", "-g", help="The role of the user.",
              type=click.Choice(["admin", "super_mod", "mod", "member"]))
def change_user(username, password, email, role):
    """Updates an user. Omit any options to use the interactive mode."""

    user = prompt_save_user(username, password, email, role)
    if user is None:
        raise FlaskCLIError("The user with username {} does not exist."
                            .format(username), fg="red")

    click.secho("[+] User {} updated.".format(user.username), fg="cyan")


@users.command("delete")
@click.option("--username", "-u", help="The username of the user.")
@click.option("--force", "-f", default=False, is_flag=True,
              help="Removes the user without asking for confirmation.")
def delete_user(username, force):
    """Deletes an user."""
    if not username:
        username = click.prompt(
            click.style("Username", fg="magenta"), type=str,
            default=os.environ.get("USER", "")
        )

    user = User.query.filter_by(username=username).first()
    if user is None:
        raise FlaskCLIError("The user with username {} does not exist."
                            .format(username), fg="red")

    if not force and not \
            click.confirm(click.style("Are you sure?", fg="magenta")):
        sys.exit(0)

    user.delete()
    click.secho("[+] User {} deleted.".format(user.username), fg="cyan")
