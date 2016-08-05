#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

image_api = Blueprint('image_api', __name__, url_prefix='/api/images')
image_view = Blueprint('image_view', __name__)
