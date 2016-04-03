#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

setting = Blueprint('setting', __name__, url_prefix='/settings')
