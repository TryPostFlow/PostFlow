#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import Schema, fields, post_load
from postflow.utils.schema import BaseSchema, update_object


class ImageSchema(Schema):
    url = fields.String(dump_only=True, allow_none=True)
    filename = fields.String(allow_none=True)
