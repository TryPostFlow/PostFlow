#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
from flask import request, current_app, jsonify
from werkzeug.utils import secure_filename
from planet.helpers.text import uniquify
from planet.extensions import storage

from planet.images import image_api


@image_api.route('', methods=["POST"])
def upload():
    image_data = request.files.get('image')

    filename = secure_filename(image_data.filename)

    folder = datetime.datetime.now().strftime('%Y/%m')
    filename = os.path.join(folder, filename)
    base_path = os.path.join(storage.base_path, storage.base_dir)
    full_path = os.path.join(base_path, filename)
    full_path = uniquify(full_path, '-')
    filename = full_path.split(base_path)[-1]
    filename = storage.save(image_data, filename=filename)
    url = storage.url(filename)
    return jsonify(
        filename=filename,
        url=url)
