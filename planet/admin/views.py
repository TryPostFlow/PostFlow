# -*- coding: utf-8 -*-

import os
from flask import send_from_directory, current_app

from . import admin_view


@admin_view.route('/admin/dist/<path:path>')
def static(path=None):
    return send_from_directory(
        current_app.static_folder, 'admin/dist/'+path)


@admin_view.route('/admin')
@admin_view.route('/admin/<path:path>')
def show(path=None):
    return send_from_directory(
        current_app.static_folder, 'admin/index.html')

