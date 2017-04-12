# -*- coding: utf-8 -*-

from flask import send_from_directory

from postflow.admin import admin_view


@admin_view.route('/assets/<path:path>')
def send_static(path=None):
    return send_from_directory(
        admin_view.root_path, 'static/assets/'+path)


@admin_view.route('/admin')
@admin_view.route('/admin/<path:path>')
def show(path=None):
    return send_from_directory(
        admin_view.root_path, 'static/index.html')
