#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import fields, post_load, pre_load
from .models import Tag
from ..helpers.text import slugify
from ..schema import BaseSchema, update_object


class TagSchema(BaseSchema):
    id = fields.Integer(allow_none=True)
    name = fields.String(required=True)
    slug = fields.String(allow_none=True)
    description = fields.String(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    @pre_load
    def slugify_name(self, in_data):
        in_data['slug'] = slugify(in_data['slug'])\
            if 'slug' in in_data.keys() else slugify(in_data['name'])

    @post_load
    def make_object(self, data):
        if data.get('id'):
            tag = Tag.query.get(data.get('id'))
            return update_object(tag, data)
        return Tag(**data)
