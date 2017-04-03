# -*- coding: utf-8 -*-

import click

from planet.utils.permissions import Need
from planet.extensions import db
from planet.account.models import Role, Permission
from planet.commands import planet


@planet.group()
def permissions():
    """Create, update or delete users."""
    pass


def init_permissions():
    admin = Role.query.filter_by(slug='admin').first()
    if not admin:
        admin = Role(name='Admin', slug='admin')
    for need in Need.needs:
        permission = Permission.query.filter(
            Permission.object_type == need.method,
            Permission.action_type == need.value).first()
        if not permission:
            permission = Permission(
                object_type=need.method, action_type=need.value)
            db.session.add(permission)
        admin.permissions.append(permission)
    db.session.add(admin)
    db.session.commit()


@permissions.command("init")
def init():
    """Creates a new user. Omit any options to use the interactive mode."""
    click.secho("[+] Initialize permissions", fg="cyan")
    init_permissions()
    click.secho("[+] Initialize permissions successfully", fg="green")
