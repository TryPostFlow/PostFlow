#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import fields, post_load, pre_load
from .models import Post
from ..account.schemas import AccountSchema
from ..tag.schemas import TagSchema
from ..helpers.text import slugify
from ..schema import BaseSchema, update_object


class PostSchema(BaseSchema):
    id = fields.Integer()
    title = fields.String(required=True)
    slug = fields.String()
    author = fields.Nested(AccountSchema, exclude=('password', ))
    markdown = fields.String()
    content = fields.String()
    tags = fields.Nested(TagSchema, many=True, partial=True)
    status = fields.String()
    views = fields.Integer()

    # @pre_load
    # def slugify_name(self, in_data):
    #     in_data['slug'] = slugify(in_data['slug'])\
    #         if 'slug' in in_data.keys() else slugify(in_data['title'])

    @post_load
    def make_object(self, data):
        if data.get('id'):
            post = Post.query.get(data.get('id'))
            return update_object(post, data)
        return Post(**data)
