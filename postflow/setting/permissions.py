#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from flask_principal import Permission
from postflow.utils.permissions import Need

SettingNeed = partial(Need, 'setting', method_name="Setting")

setting_list_perm = Permission(SettingNeed('list', value_name="List Settings"))
setting_show_perm = Permission(SettingNeed('show', value_name="Show Setting"))
setting_update_perm = Permission(
    SettingNeed('update', value_name="Edit Setting"))
