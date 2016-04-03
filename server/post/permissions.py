#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from flask_principal import Permission

from ..permissions import Need

PostNeed = partial(Need, 'post')

post_index_perm = Permission(PostNeed('index'))
post_show_perm = Permission(PostNeed('show'))
post_create_perm = Permission(PostNeed('show'))
post_update_perm = Permission(PostNeed('update'))
post_destory_perm = Permission(PostNeed('destory'))
