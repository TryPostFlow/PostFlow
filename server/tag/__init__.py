#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint


api = Blueprint('tag_api', __name__, url_prefix='/tags')
