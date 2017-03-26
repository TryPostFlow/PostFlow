#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from flask_principal import Permission
from planet.utils.permissions import Need

SettingNeed = partial(Need, 'setting')

setting_list_perm = Permission(SettingNeed('list'))
setting_show_perm = Permission(SettingNeed('show'))
setting_update_perm = Permission(SettingNeed('update'))
