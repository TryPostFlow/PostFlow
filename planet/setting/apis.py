#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from planet.utils.schema import render_schema, render_error
from planet.utils.permissions import auth
from planet.setting import setting_api
from planet.setting.schemas import SettingSchema
from planet.setting.models import get_setting, get_all_settings, save_setting
from planet.setting.permissions import (setting_list_perm, setting_show_perm,
                                        setting_update_perm)


@setting_api.route('', methods=['GET'])
@auth.require(401)
@setting_list_perm.require(403)
def index():
    settings = get_all_settings()
    return render_schema(settings, SettingSchema())


@setting_api.route('/<id_or_key>', methods=['GET'])
@auth.require(401)
@setting_show_perm.require(403)
def show(id_or_key):
    setting = get_setting(id_or_key)
    return render_schema(setting, SettingSchema())


@setting_api.route('', methods=['PUT'])
@auth.require(401)
@setting_update_perm.require(403)
def update():
    payload = request.get_json()
    if not payload:
        return render_error(20001, 'No input data provided')
    settings = []
    for key in payload:
        item = payload[key]
        if 'key' in item.keys():
            setting = save_setting(item['key'], item.get('value'))
            settings.append(setting)
    return render_schema(settings, SettingSchema())
