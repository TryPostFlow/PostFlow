#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import time
from flask import request, jsonify
from werkzeug.utils import secure_filename
from planet.extensions import storage
from planet.image import image_api


@image_api.route('', methods=["POST"])
def upload():
    image_data = request.files.get('image')

    filename = secure_filename(image_data.filename)

    folder = datetime.datetime.now().strftime('%Y/%m')
    filename = os.path.join(folder, filename)
    unique_key = str(int(time.time() * 1000))[-10:]
    basename, ext = os.path.splitext(filename)
    filename = '{}-{}{}'.format(basename, unique_key, ext)
    filename = storage.save(image_data, filename=filename)
    url = storage.url(filename)
    return jsonify(
        filename=filename,
        url=url)
