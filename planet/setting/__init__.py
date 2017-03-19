#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

setting_api = Blueprint('setting_api', __name__, url_prefix='/api/settings')
