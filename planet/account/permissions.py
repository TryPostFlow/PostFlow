#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from flask_principal import Permission

from planet.utils.permissions import Need

AccountNeed = partial(Need, 'account')

account_list_perm = Permission(AccountNeed('list'))
account_show_perm = Permission(AccountNeed('show'))
account_create_perm = Permission(AccountNeed('create'))
account_update_perm = Permission(AccountNeed('update'))
account_destory_perm = Permission(AccountNeed('destory'))

RoleNeed = partial(Need, 'role')

role_list_perm = Permission(RoleNeed('list'))
role_show_perm = Permission(RoleNeed('show'))
role_create_perm = Permission(RoleNeed('create'))
role_update_perm = Permission(RoleNeed('update'))
role_destory_perm = Permission(RoleNeed('destory'))