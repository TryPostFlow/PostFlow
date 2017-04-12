#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from flask_principal import Permission
from postflow.utils.permissions import Need

PostNeed = partial(Need, 'tag', method_name="Tag")

tag_list_perm = Permission(PostNeed('list', value_name="List Tags"))
tag_show_perm = Permission(PostNeed('show', value_name="Show Tag"))
tag_create_perm = Permission(PostNeed('create', value_name="Create Tag"))
tag_update_perm = Permission(PostNeed('update', value_name="Edit Tag"))
tag_destory_perm = Permission(PostNeed('destory', value_name="Delete Tag"))
