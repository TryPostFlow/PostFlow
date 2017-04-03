#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

account_view = Blueprint('account_view', __name__)
account_api = Blueprint('account_api', __name__, url_prefix='/api')

role_api = Blueprint('role_api', __name__, url_prefix='/api')