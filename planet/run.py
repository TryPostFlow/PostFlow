#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import create_app

packages = [
    'account',
    'auth',
    'post',
    'tag'
]

app = create_app(packages=packages)

if __name__ == '__main__':
    app.run()
