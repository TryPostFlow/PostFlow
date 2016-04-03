#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import Schema, fields
from .models import Media


class MediaSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    content = fields.String()
    url = fields.String()
    status = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    def make_object(self, data):
        return Media(**data)
