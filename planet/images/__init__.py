#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

image_view = Blueprint('image_view', __name__, url_prefix='/api/images')
