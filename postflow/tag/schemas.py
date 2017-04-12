#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import fields, post_load
from postflow.utils.schema import BaseSchema, update_object
from postflow.image.schemas import ImageSchema
from postflow.tag.models import Tag


class TagSchema(BaseSchema):
    id = fields.Integer(allow_none=True)
    name = fields.String()
    slug = fields.String(allow_none=True)
    description = fields.String(allow_none=True)
    image = fields.Nested(ImageSchema)
    num_posts = fields.Integer(allow_none=True, dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        model = Tag

    def get_instance(self, data):
        """Retrieve an existing record by primary key(s)."""
        if not self.opts.model:
            return None
        return self.opts.model.query.filter_by(name=data.get('name')).first()
