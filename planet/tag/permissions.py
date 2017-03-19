#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from flask_principal import Permission

from planet.utils.permissions import Need

PostNeed = partial(Need, 'tag')

tag_list_perm = Permission(PostNeed('list'))
tag_show_perm = Permission(PostNeed('show'))
tag_create_perm = Permission(PostNeed('create'))
tag_update_perm = Permission(PostNeed('update'))
tag_destory_perm = Permission(PostNeed('destory'))
