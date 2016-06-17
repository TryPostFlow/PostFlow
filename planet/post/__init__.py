#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

api = Blueprint('post_api', __name__, url_prefix='/posts')
