#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint


tag_api = Blueprint('tag_api', __name__, url_prefix='/api/tags')
tag_view = Blueprint('tag_view', __name__)
