# -*- coding: utf-8 -*-

import dateutil
from flask import current_app, g
from flask_themes2 import get_theme, render_theme_template


def get_current_theme():
    theme = current_app.config['THEME']
    return get_theme(theme)


def render_template(template, **context):
    return render_theme_template(get_current_theme(), template, **context)


def format_datetime(value, format='%Y-%m-%dT%H:%M:%SZ'):
    date = dateutil.parser.parse(value)
    native = date.replace(tzinfo=None)
    return native.strftime(format)
