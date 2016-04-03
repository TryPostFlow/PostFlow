#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getpass

from flask.ext.script import Command  # , Shell, prompt, prompt_pass
from .extensions import db
from .account.models import create_user, Permission
from .permissions import Need


class CreateDBCommand(Command):
    def run(self):
        db.create_all()


class DropDBCommand(Command):
    def run(self):
        db.drop_all()


def _make_context():
    return dict(db=db)


class CreateSuperUserCommand(Command):
    def run(self):
        cmd = raw_input('Create superuser?(Y/n): ')
        if cmd == 'n':
            sys.exit(1)
        name = raw_input('name: ')
        email = raw_input('email: ')
        password = getpass.getpass('password: ')
        create_user(name=name,
                    email=email,
                    password=password)


class RegisterActionsCommand(Command):
    def run(self):
        for need in Need._needs:
            db.session.add(
                Permission(object_type=need.method, action_type=need.value))
        db.session.commit()
        print 'over'
