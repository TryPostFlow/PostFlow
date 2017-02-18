#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import jwt
# import calendar
# import datetime
from flask import request, g

from . import account_api
from .schemas import AccountSchema, PasswordSchema
from .models import get_user, get_all_users
from ..permissions import auth
from .permissions import (
    account_list_perm, account_show_perm, account_create_perm,
    account_update_perm, account_destory_perm)

from ..schema import render_schema, render_error
from ..extensions import db


@account_api.route('/me', methods=['GET'])
@auth.require(401)
def me():
    return render_schema(g.user, AccountSchema)


@account_api.route('/<int:id>', methods=['GET'])
@auth.require(401)
@account_show_perm.require(403)
def view(id):
    user = get_user(id)
    return render_schema(user, AccountSchema)


@account_api.route('', methods=['GET'])
@auth.require(401)
@account_list_perm.require(403)
def list():
    page = int(request.values.get('p', 1))
    limit = int(request.values.get('limit', 20))
    users = get_all_users(page, limit)
    return render_schema(users, AccountSchema)


@account_api.route('', methods=['POST'])
@auth.require(401)
@account_create_perm.require(403)
def create():
    payload = request.get_json()
    account_schema = AccountSchema(only=('name', 'email', 'password'))
    account_data, errors = account_schema.load(payload)
    if errors:
        return render_error(20001, errors, 422)
    db.session.add(account_data)
    db.session.commit()
    return render_schema(account_data, AccountSchema)


@account_api.route('/<int:id>/password', methods=['PUT'])
@auth.require(401)
@account_update_perm.require(403)
def update_password(id):
    payload = request.get_json()
    password_schema = PasswordSchema()
    password_data, errors = password_schema.load(payload)
    if errors:
        return render_error(20001, errors, 422)
    user = get_user(id)
    user.password = password_data['new_password']
    db.session.add(user)
    db.session.commit()
    message = {
        'code': 10000,
        'message': 'success'
    }
    return render_schema(message)


@account_api.route('/<int:id>', methods=['PUT'])
@auth.require(401)
@account_update_perm.require(403)
def update(id):
    payload = request.get_json()
    account_schema = AccountSchema(only=('id', 'name', 'email', 'password'))
    account_data, errors = account_schema.load(payload)
    if errors:
        return render_error(20001, errors, 422)
    db.session.add(account_data)
    db.session.commit()
    return render_schema(account_data, AccountSchema)


@account_api.route('/<id>', methods=['DELETE'])
@auth.require(401)
@account_destory_perm.require(403)
def destory(id):
    account = get_user(id)
    db.session.delete(account)
    db.session.commit()

    message = {
        'code': 10000,
        'message': 'success'
    }

    return render_schema(message)