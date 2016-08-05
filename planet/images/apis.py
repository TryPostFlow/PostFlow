#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
from flask import request, current_app, jsonify, url_for
from werkzeug.utils import secure_filename
from ..helpers.text import uniquify

from . import image_api


@image_api.route('/upload', methods=["POST"])
def upload():
    image = request.files['image']
    filename = secure_filename(image.filename)
    now = datetime.datetime.now()
    folder = now.strftime('%Y/%m')
    full_folder = os.path.join(current_app.config['IMAGE_PATHS'], folder)
    if not os.path.exists(full_folder):
        os.makedirs(full_folder)
    full_path = uniquify(os.path.join(full_folder, filename), '-')
    image.save(full_path)
    return jsonify(
        path=url_for(
            'image_view.show',
            path=os.path.join(folder, os.path.basename(full_path)),
            _external=True))
