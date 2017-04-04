#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import fields, post_load
from planet.utils.schema import BaseSchema, update_object
from planet.tag.models import Tag


class TagSchema(BaseSchema):
    id = fields.Integer(allow_none=True)
    name = fields.String()
    slug = fields.String(allow_none=True)
    description = fields.String(allow_none=True)
    image = fields.String(dump_only=True, allow_none=True)
    _image = fields.String(allow_none=True)
    num_posts = fields.Integer(allow_none=True, dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_object(self, data):
        if data.get('id'):
            tag = Tag.query.get(data.get('id'))
            return update_object(tag, data)
        return Tag(**data)
