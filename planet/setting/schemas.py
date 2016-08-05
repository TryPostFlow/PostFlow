#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import fields, post_load
from .models import Setting, get_setting
from ..helpers.text import slugify
from ..schema import BaseSchema, update_object


class SettingSchema(BaseSchema):
    id = fields.Integer()
    key = fields.String(required=True)
    value = fields.String()

    @post_load
    def make_object(self, data):
        if data.get('id'):
            post = get_setting(data.get('id'))
            return update_object(post, data)
        return Setting(**data)
