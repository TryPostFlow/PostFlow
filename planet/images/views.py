# -*- coding: utf-8 -*-

import os
from flask import send_from_directory, current_app

from . import image_view


@image_view.route('/content/images/<path:path>')
def show(path):
    return send_from_directory(
        os.path.join(
            current_app.instance_path,
            current_app.config['IMAGE_PATHS']), path)
