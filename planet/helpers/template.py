# -*- coding: utf-8 -*-

import dateutil
from flask import current_app, g
from flask_themes import render_theme_template


def get_theme():
    return g.site.activeTheme or current_app.config['THEME']


def render_template(template, **context):
    return render_theme_template(get_theme(), template, **context)


def format_datetime(value, format='%Y-%m-%dT%H:%M:%SZ'):
    date = dateutil.parser.parse(value)
    native = date.replace(tzinfo=None)
    return native.strftime(format)
