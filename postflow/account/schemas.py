#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshmallow import (Schema, fields, validates_schema, ValidationError,
                         post_load, validates, pre_load)
from postflow.utils.schema import BaseSchema
from postflow.account.models import User, Role, Permission


class PermissionSchema(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    object_type = fields.String()
    action_type = fields.String()
    action_name = fields.String()
    object_id = fields.Integer()

    class Meta():
        model = Permission

    def get_instance(self, data):
        if data.get('id'):
            return Permission.query.get(data['id'])
        elif data.get('object_type') and data.get('action_type'):
            return Permission.query.filter(
                Permission.object_type == data.get('object_type'),
                Permission.action_type == data.get('action_type')).first()
        return None


class GroupPermissionSchema(BaseSchema):
    name = fields.String()
    object_type = fields.String()
    permissions = fields.Nested(
        PermissionSchema,
        many=True,
        only=('id', 'object_type', 'action_type', 'action_name'))


class RoleSchema(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    slug = fields.String()
    description = fields.String()
    permissions = fields.Nested(
        PermissionSchema,
        many=True,
        only=('id', 'object_type', 'action_type', 'action_name'))
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta():
        model = Role


class AccountSchema(BaseSchema):
    id = fields.Integer()
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True, required=True)
    avatar = fields.String()
    primary_role = fields.Nested(
        RoleSchema, exclude=('permissions', ), required=True)
    status = fields.String()
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta():
        model = User

    @validates_schema(skip_on_field_errors=True)
    def validate_name(self, data):
        # if not data.get('name'):
        #     raise ValidationError("The name is needed", "name")
        account = User.query.filter(User.name == data.get('name')).first()
        if data.get('id') and account and\
                str(data.get('id')) != str(account.id):
            raise ValidationError("This name has existed", "name")
        if not data.get('id') and account:
            raise ValidationError("This name has existed", "name")

    @validates_schema(skip_on_field_errors=True)
    def validate_email(self, data):
        # if not data.get('email'):
        #     raise ValidationError("The email is needed", "email")
        account = User.query.filter(User.email == data.get('email')).first()
        if data.get('id') and account and\
                str(data.get('id')) != str(account.id):
            raise ValidationError("This email has existed", "email")
        if not data.get('id') and account:
            raise ValidationError("This email has existed", "email")


class PasswordSchema(BaseSchema):
    id = fields.Integer()
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
