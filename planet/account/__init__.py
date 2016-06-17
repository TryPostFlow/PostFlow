#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

frontend = Blueprint('account_frontend', __name__)
api = Blueprint('account_api', __name__, url_prefix='/accounts')
