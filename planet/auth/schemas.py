#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import (
    Schema, fields, validates_schema, ValidationError, post_load, validates)
from planet.account.models import User


class LoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)

    @validates('email')
    def validate_account(self, email):
        account = User.query.filter_by(email=email).first()
        if not account:
            raise ValidationError("This account doesn't exist")

    @post_load
    def make_account(self, data):
        return User.query.filter_by(email=data.get('email')).first()

    @validates_schema
    def validate_login(self, data):
        account = User.query.filter(
            User.email == data.get('email')).first()
        authenticated = account.check_password(data.get('password')) if account else False
        if not authenticated:
            raise ValidationError("account or password is wrong")
