#!/usr/bin/env python
# coding=utf-8

from flask_mail import Mail
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal
from flask_oauthlib.provider import OAuth2Provider

__all__ = ['mail', 'db', 'cache', 'principals', 'oauth']

mail = Mail()
db = SQLAlchemy()
cache = Cache()
principals = Principal(use_sessions=False)
oauth = OAuth2Provider()
