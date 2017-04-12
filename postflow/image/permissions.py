#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from flask_principal import Permission
from postflow.utils.permissions import Need

ImageNeed = partial(Need, 'image', method_name="Image")

image_upload_perm = Permission(ImageNeed('upload', value_name="Image Upload"))
