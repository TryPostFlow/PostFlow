#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

admin_view = Blueprint('admin_view', __name__, template_folder='static', static_url_path='')
