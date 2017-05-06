#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, abort
from postflow.utils.permissions import auth
from postflow.setting import setting_api
from postflow.setting.schemas import SettingSchema
from postflow.setting.models import get_setting, get_all_settings, save_setting
from postflow.setting.permissions import (setting_list_perm, setting_show_perm,
                                          setting_update_perm)


@setting_api.route('', methods=['GET'])
@auth.require(401)
@setting_list_perm.require(403)
def index():
    settings_data = get_all_settings()
    return SettingSchema().jsonify(settings_data)


@setting_api.route('/<setting_id>', methods=['GET'])
@auth.require(401)
@setting_show_perm.require(403)
def show(setting_id):
    setting_data = get_setting(setting_id)
    if not setting_data:
        abort(404)
    return SettingSchema().jsonify(setting_data)


@setting_api.route('', methods=['PUT'])
@auth.require(401)
@setting_update_perm.require(403)
def update():
    payload = request.get_json()
    settings = []
    for key in payload:
        item = payload[key]
        if 'key' in item.keys():
            setting = save_setting(item['key'], item.get('value'))
            settings.append(setting)
    return SettingSchema().jsonify(settings)
