#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, g

from planet.extensions import db
from planet.utils.schema import render_schema, render_error
from planet.utils.permissions import auth
from planet.account import account_api
from planet.account.schemas import AccountSchema, PasswordSchema, RoleSchema
from planet.account.models import (User, get_user, get_all_users, get_role)
from planet.account.permissions import (
    account_list_perm, account_show_perm, account_create_perm,
    account_update_perm, account_destory_perm)


@account_api.route('/accounts/me', methods=['GET'])
@auth.require(401)
def me():
    return render_schema(g.user, AccountSchema)


@account_api.route('/accounts/<int:id>', methods=['GET'])
@auth.require(401)
@account_show_perm.require(403)
def view(id):
    user = get_user(id)
    return render_schema(user, AccountSchema)


@account_api.route('/accounts', methods=['GET'])
@auth.require(401)
@account_list_perm.require(403)
def index():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    role_id = request.args.get('role')
    users_query = User.query
    if role_id:
        role = get_role(role_id)
        if role:
            users_query = users_query.filter(
                db.or_(
                    User.primary_role == role,
                    User.secondary_roles.any(id=role.id)))
    users = users_query.order_by(User.created_at.desc()).paginate(page, limit)

    return render_schema(users, AccountSchema)


@account_api.route('/accounts', methods=['POST'])
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


@account_api.route('/accounts/<int:id>/password', methods=['PUT'])
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
    message = {'code': 10000, 'message': 'success'}
    return render_schema(message)


@account_api.route('/accounts/<int:id>', methods=['PUT'])
@auth.require(401)
@account_update_perm.require(403)
def update(id):
    payload = request.get_json()
    account_schema = AccountSchema(only=('id', 'name', 'email', 'primary_role',
                                         'status'))
    account_data, errors = account_schema.load(payload)
    if errors:
        return render_error(20001, errors, 422)
    db.session.add(account_data)
    db.session.commit()
    return render_schema(account_data, AccountSchema)


@account_api.route('/accounts/<id>', methods=['DELETE'])
@auth.require(401)
@account_destory_perm.require(403)
def destory(id):
    account = get_user(id)
    db.session.delete(account)
    db.session.commit()

    message = {'code': 10000, 'message': 'success'}

    return render_schema(message)
