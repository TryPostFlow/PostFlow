#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

post_api = Blueprint('post_api', __name__, url_prefix='/api/posts')
post_view = Blueprint('post_view', __name__)
