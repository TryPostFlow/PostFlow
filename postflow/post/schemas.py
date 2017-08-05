#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import fields
from postflow.utils.schema import BaseSchema
from postflow.post.models import Post
from postflow.account.schemas import AccountSchema
from postflow.tag.schemas import TagSchema
from postflow.image.schemas import ImageSchema


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
    telegram = fields.Integer(dump_only=True)
    status = fields.String()
    views = fields.Integer(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
