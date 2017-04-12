# -*- coding: utf-8 -*-

import os
import sys
import click

from sqlalchemy.exc import IntegrityError
from postflow.account.models import User
from postflow.commands import postflow
from postflow.commands.utils import (EmailType, prompt_save_user, FlaskCLIError)


@postflow.group()
def users():
    """Create, update or delete users."""
    pass


@users.command("new")
@click.option("--name", "-u", help="The name of the user.")
@click.option("--email", "-e", type=EmailType(),
              help="The email address of the user.")
@click.option("--password", "-p", help="The password of the user.")
@click.option("--role", "-r", help="The role of the user.",
              type=click.Choice(["admin", "super_mod", "mod", "member"]))
def new_user(name, email, password, role):
    """Creates a new user. Omit any options to use the interactive mode."""
    try:
        user = prompt_save_user(name, email, password, role)

        click.secho("[+] User {} with Email {} in Role {} created.".format(
            user.name, user.email, user.primary_role.name), fg="cyan")
    except IntegrityError:
        raise FlaskCLIError("Couldn't create the user because the "
                            "name or email address is already taken.",
                            fg="red")


@users.command("update")
@click.option("--name", "-u", help="The name of the user.")
@click.option("--email", "-e", type=EmailType(),
              help="The email address of the user.")
@click.option("--password", "-p", help="The password of the user.")
@click.option("--role", "-g", help="The role of the user.",
              type=click.Choice(["admin", "super_mod", "mod", "member"]))
def change_user(name, password, email, role):
    """Updates an user. Omit any options to use the interactive mode."""

    user = prompt_save_user(name, password, email, role)
    if user is None:
        raise FlaskCLIError("The user with name {} does not exist."
                            .format(name), fg="red")

    click.secho("[+] User {} updated.".format(user.name), fg="cyan")


@users.command("delete")
@click.option("--name", "-u", help="The name of the user.")
@click.option("--force", "-f", default=False, is_flag=True,
              help="Removes the user without asking for confirmation.")
def delete_user(name, force):
    """Deletes an user."""
    if not name:
        name = click.prompt(
            click.style("Name", fg="magenta"), type=str,
            default=os.environ.get("USER", "")
        )

    user = User.query.filter_by(name=name).first()
    if user is None:
        raise FlaskCLIError("The user with name {} does not exist."
                            .format(name), fg="red")

    if not force and not \
            click.confirm(click.style("Are you sure?", fg="magenta")):
        sys.exit(0)

    user.delete()
    click.secho("[+] User {} deleted.".format(user.name), fg="cyan")
