#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import fields
from planet.utils.schema import BaseSchema
from planet.setting.models import Setting


class SettingSchema(BaseSchema):
    id = fields.Integer()
    key = fields.String(required=True)
    value = fields.String()

    class Meta():
        model = Setting
