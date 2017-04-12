#!/usr/bin/env python
# coding=utf-8

from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_storage import Storage
from flask_alembic import Alembic
from flask_principal import Principal
from flask_oauthlib.provider import OAuth2Provider
from flask_themes2 import Themes
from raven.contrib.flask import Sentry

__all__ = ['mail', 'db', 'storage','alembic', 'principals', 'oauth', 'sentry']

mail = Mail()
db = SQLAlchemy()
principals = Principal(use_sessions=False)
oauth = OAuth2Provider()
sentry = Sentry()
alembic = Alembic()
storage = Storage()
themes = Themes()
