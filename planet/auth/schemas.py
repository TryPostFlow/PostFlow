#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import (
    Schema, fields, validates_schema, ValidationError, post_load, validates)
from .models import User
from ..schema import BaseSchema, update_object


class ClientSchema(BaseSchema):
    name = fields.String()
    email = fields.Email()
    password = fields.String()

    @post_load
    def make_object(self, data):
        if data.get('id'):
            user = User.query.get(data.get('id'))
            return update_object(user, data)
        return User(**data)

    @validates_schema
    def validate_email(self, data):
        account = User.query.filter(
            User.email == data.get('email')).first()

        if data.get('id') and account and data.get('id') != str(account.id):
            raise ValidationError("This email has existed")
        if not data.get('id') and account:
            raise ValidationError("This email has existed")