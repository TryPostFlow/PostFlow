#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import (
    Schema, fields, validates_schema, ValidationError, post_load, validates)
from planet.utils.schema import BaseSchema, update_object
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

    @post_load
    def validate_login(self, data):
        account = User.query.filter(
            User.email == data.get('email')).first()
        authenticated = account.check_password(data.get('password'))\
            if account else False
        if not authenticated:
            raise ValidationError("account or password is wrong")


class AccountSchema(BaseSchema):
    name = fields.String()
    email = fields.Email()
    avatar = fields.String()

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
        if data.get('id') and account and\
                str(data.get('id')) != str(account.id):
            raise ValidationError("This email has existed")
        if not data.get('id') and account:
            raise ValidationError("This email has existed")


class PasswordSchema(BaseSchema):
    old_password = fields.String(required=True)
    new_password = fields.String(required=True)
    verify_password = fields.String(required=True)

    @validates_schema
    def validate_old_password(self, data):
        user = User.query.get(data.get('id'))
        if not user:
            raise ValidationError("This account doesn't exist")
        if not user.check_password(data.get('old_password')):
            raise ValidationError("The old password is wrong", field_names=['old_password', ])

    @validates_schema
    def validate_new_password(self, data):
        if data.get('new_password') != data.get('verify_password'):
            raise ValidationError("Your new password do not match", field_names=['verify_password', ])
