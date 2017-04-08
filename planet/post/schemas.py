#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import fields
from planet.utils.schema import BaseSchema
from planet.post.models import Post
from planet.account.schemas import AccountSchema
from planet.tag.schemas import TagSchema
from planet.image.schemas import ImageSchema


class PostSchema(BaseSchema):
    class Meta():
        model = Post

    id = fields.Integer()
    title = fields.String(required=True)
    slug = fields.String()
    author = fields.Nested(AccountSchema, only=('id', 'name'))
    markdown = fields.String()
    content = fields.String()
    image = fields.Nested(ImageSchema)
    tags = fields.Nested(
        TagSchema, only=('id', 'name', 'slug'), many=True, partial=True)
    status = fields.String()
    views = fields.Integer(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
