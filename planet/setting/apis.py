#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from . import setting
from ..schema import render_schema, render_error
from .schemas import SettingSchema
from .models import get_setting, get_all_settings, save_setting


@setting.route('', methods=['GET'])
def index():
    settings = get_all_settings()
    return render_schema(settings, SettingSchema)


@setting.route('/<id_or_key>', methods=['GET'])
def show(id_or_key):
    setting = get_setting(id_or_key)
    return render_schema(setting, SettingSchema)


@setting.route('', methods=['PUT'])
def update():
    payload = request.get_json()
    if not payload:
        return render_error(20001, 'No input data provided')
    settings = []
    for key in payload:
        item = payload[key]
        print item
        if 'key' in item.keys():
            setting = save_setting(item['key'], item.get('value'))
            settings.append(setting)
    return render_schema(settings, SettingSchema)
