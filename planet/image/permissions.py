#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from flask_principal import Permission
from planet.utils.permissions import Need

ImageNeed = partial(Need, 'image')

image_upload_perm = Permission(ImageNeed('upload'))
