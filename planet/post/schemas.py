#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import fields, post_load
from planet.utils.schema import BaseSchema, update_object
from planet.post.models import Post
from planet.account.schemas import AccountSchema
from planet.tag.schemas import TagSchema


class PostSchema(BaseSchema):
    id = fields.Integer()
    title = fields.String(required=True)
    slug = fields.String()
    author = fields.Nested(AccountSchema, exclude=('password', ))
    markdown = fields.String()
    content = fields.String()
    image = fields.String(dump_only=True, allow_none=True)
    _image = fields.String(allow_none=True)
    tags = fields.Nested(TagSchema, many=True, partial=True)
    status = fields.String()
    views = fields.Integer()

    @post_load
    def make_object(self, data):
        if data.get('id'):
            post = Post.query.get(data.get('id'))
            return update_object(post, data)
        return Post(**data)
