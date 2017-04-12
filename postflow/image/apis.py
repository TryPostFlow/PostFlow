#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import time
from flask import request, jsonify
from werkzeug.utils import secure_filename
from postflow.extensions import storage
from postflow.utils.permissions import auth
from postflow.image import image_api
from postflow.image.permissions import image_upload_perm


@image_api.route('', methods=["POST"])
@auth.require(401)
@image_upload_perm.require(403)
def upload():
    image_data = request.files.get('file')

    filename = secure_filename(image_data.filename)

    folder = datetime.datetime.now().strftime('%Y/%m')
    filename = os.path.join(folder, filename)
    unique_key = str(int(time.time() * 1000))[-10:]
    basename, ext = os.path.splitext(filename)
    filename = '{}-{}{}'.format(basename, unique_key, ext)
    filename = storage.save(image_data, filename=filename)
    url = storage.url(filename)
    return jsonify(filename=filename, url=url)
