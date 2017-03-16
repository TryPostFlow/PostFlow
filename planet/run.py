#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werkzeug.contrib.fixers import ProxyFix
from planet import create_app

app = create_app()
# app.wsgi_app = ProxyFix(app.wsgi_app)
