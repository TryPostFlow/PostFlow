#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from flask_principal import Permission

from postflow.utils.permissions import Need

AccountNeed = partial(Need, 'account', method_name="Account")

account_list_perm = Permission(AccountNeed('list', value_name="List Accounts"))
account_show_perm = Permission(AccountNeed('show', value_name="Show Account"))
account_create_perm = Permission(
    AccountNeed('create', value_name="Create Account"))
account_update_perm = Permission(
    AccountNeed('update', value_name="Edit Account"))
account_destory_perm = Permission(
    AccountNeed('destory', value_name="Delete Account"))

RoleNeed = partial(Need, 'role', method_name="Role")

role_list_perm = Permission(RoleNeed('list', value_name="List Roles"))
role_show_perm = Permission(RoleNeed('show', value_name="Show Role"))
role_create_perm = Permission(RoleNeed('create', value_name="Create Role"))
role_update_perm = Permission(RoleNeed('update', value_name="Edit Role"))
role_destory_perm = Permission(RoleNeed('destory', value_name="Delete Role"))