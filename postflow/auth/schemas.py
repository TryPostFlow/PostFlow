#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import (Schema, fields, validates_schema, ValidationError,
                         post_load, validates)
from postflow.account.models import User
from postflow.utils.schema import BaseSchema


class LoginSchema(BaseSchema):
    email = fields.String(required=True)
    password = fields.String(required=True)

    @validates('email')
    def validate_account(self, email):
        account = User.query.filter_by(email=email).first()
        if not account:
            raise ValidationError("This account doesn't exist")

    def get_instance(self, data):
        """Retrieve an existing record by primary key(s)."""
        return User.query.filter_by(email=data.get('email')).first()

    @validates_schema
    def validate_login(self, data):
        account = User.query.filter(User.email == data.get('email')).first()
        authenticated = account.check_password(
            data.get('password')) if account else False
        if not authenticated:
            raise ValidationError("account or password is wrong")
