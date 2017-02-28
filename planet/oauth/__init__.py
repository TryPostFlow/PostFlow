#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

oauth_api = Blueprint('oauth_api', __name__, url_prefix='/api/oauth')
