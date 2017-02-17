#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from flask_principal import Permission

from ..permissions import Need

AccountNeed = partial(Need, 'account')

account_list_perm = Permission(AccountNeed('list'))
account_show_perm = Permission(AccountNeed('show'))
account_create_perm = Permission(AccountNeed('create'))
account_update_perm = Permission(AccountNeed('update'))
account_destory_perm = Permission(AccountNeed('destory'))
