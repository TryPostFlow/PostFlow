#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import fields
from postflow.utils.schema import BaseSchema
from postflow.setting.models import Setting


class SettingSchema(BaseSchema):
    id = fields.Integer()
    key = fields.String(required=True)
    value = fields.String()

    class Meta():
        model = Setting

    def get_instance(self, data):
        if data.get('id'):
            return Setting.query.get(data['id'])
        elif data.get('key'):
            return Setting.query.filter_by(key=data.get('key')).first()
        return None
