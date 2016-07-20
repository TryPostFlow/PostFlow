#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from flask_principal import Permission

from ..permissions import Need

PostNeed = partial(Need, 'post')

post_create_perm = Permission(PostNeed('create'))
post_update_perm = Permission(PostNeed('update'))
post_destory_perm = Permission(PostNeed('destory'))
