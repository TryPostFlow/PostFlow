#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from flask_principal import Permission

from planet.utils.permissions import Need

PostNeed = partial(Need, 'post')

post_list_perm = Permission(PostNeed('list'))
post_show_perm = Permission(PostNeed('show'))
post_create_perm = Permission(PostNeed('create'))
post_update_perm = Permission(PostNeed('update'))
post_destory_perm = Permission(PostNeed('destory'))
