#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werkzeug.contrib.fixers import ProxyFix
from . import create_app

packages = [
    'account',
    'oauth',
    'auth',
    'post',
    'tag',
    'setting',
    'images',
    'admin'
]

app = create_app(packages=packages)
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()
