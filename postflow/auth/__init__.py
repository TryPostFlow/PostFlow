#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

auth_api = Blueprint('auth_api', __name__, url_prefix='/api')
