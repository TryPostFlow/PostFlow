#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from flask_principal import Permission
from postflow.utils.permissions import Need

PostNeed = partial(Need, 'post', method_name="Post")

post_list_perm = Permission(PostNeed('list', value_name="List Posts"))
post_show_perm = Permission(PostNeed('show', value_name="Show Post"))
post_create_perm = Permission(PostNeed('create', value_name="Create Post"))
post_update_perm = Permission(PostNeed('update', value_name="Edit Post"))
post_destory_perm = Permission(PostNeed('destory', value_name="Delete Post"))
