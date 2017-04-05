#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import (Schema, fields, validates_schema, ValidationError,
                         post_load, validates)
from planet.utils.schema import BaseSchema, update_object
from planet.account.models import User, Role, Permission


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
        account = User.query.filter(User.email == data.get('email')).first()
        authenticated = account.check_password(data.get('password'))\
            if account else False
        if not authenticated:
            raise ValidationError("account or password is wrong")


class PermissionSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    object_type = fields.String()
    action_type = fields.String()
    action_name = fields.String()
    object_id = fields.Integer()

    @post_load
    def make_object(self, data):
        if data.get('id'):
            permission = Permission.query.get(data.get('id'))
            return permission
        return Permission(**data)


class GroupPermissionSchema(Schema):
    name = fields.String()
    object_type = fields.String()
    permissions = fields.Nested(
        PermissionSchema,
        many=True,
        only=('id', 'object_type', 'action_type', 'action_name'))


class RoleSchema(BaseSchema):
    name = fields.String()
    description = fields.String()
    permissions = fields.Nested(
        PermissionSchema,
        many=True,
        only=('id', 'object_type', 'action_type', 'action_name'))

    @post_load
    def make_object(self, data):
        if data.get('id'):
            role = Role.query.get(data.get('id'))
            if len(data.keys()) == 1:
                return role
            return update_object(role, data)
        return Role(**data)


class AccountSchema(BaseSchema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True, required=True)
    avatar = fields.String()
    primary_role = fields.Nested(
        RoleSchema,
        exclude=('permissions', 'description'),
        dump_only=('created_at', 'updated_at'))
    status = fields.String()

    @post_load
    def make_object(self, data):
        if data.get('id'):
            user = User.query.get(data.get('id'))
            return update_object(user, data)
        return User(**data)

    @validates_schema(skip_on_field_errors=True)
    def validate_name(self, data):
        if not data.get('name'):
            raise ValidationError("The name is needed", "name")
        account = User.query.filter(User.name == data.get('name')).first()
        if data.get('id') and account and\
                str(data.get('id')) != str(account.id):
            raise ValidationError("This name has existed", "name")
        if not data.get('id') and account:
            raise ValidationError("This name has existed", "name")

    @validates_schema(skip_on_field_errors=True)
    def validate_email(self, data):
        if not data.get('email'):
            raise ValidationError("The email is needed", "email")
        account = User.query.filter(User.email == data.get('email')).first()
        if data.get('id') and account and\
                str(data.get('id')) != str(account.id):
            raise ValidationError("This email has existed", "email")
        if not data.get('id') and account:
            raise ValidationError("This email has existed", "email")


class PasswordSchema(BaseSchema):
    old_password = fields.String(load_only=True, required=True)
    new_password = fields.String(load_only=True, required=True)
    verify_password = fields.String(load_only=True, required=True)

    @validates_schema
    def validate_old_password(self, data):
        user = User.query.get(data.get('id'))
        if not user:
            raise ValidationError("This account doesn't exist")
        if data.get('old_password'
                    ) and not user.check_password(data.get('old_password')):
            raise ValidationError("The old password is wrong", 'old_password')

    @validates_schema
    def validate_new_password(self, data):
        if data.get('new_password') != data.get('verify_password'):
            raise ValidationError("Your new password do not match",
                                  'verify_password')
