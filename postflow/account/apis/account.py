#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, g, jsonify, abort

from postflow.extensions import db
from postflow.utils.permissions import auth
from postflow.account import account_api
from postflow.account.schemas import AccountSchema, PasswordSchema
from postflow.account.models import User
from postflow.account.permissions import (
    account_list_perm, account_show_perm, account_create_perm,
    account_update_perm, account_destory_perm)


@account_api.route('/accounts/me', methods=['GET'])
@auth.require(401)
def me():
    return AccountSchema().jsonify(g.user)


@account_api.route('/accounts/<account_id>', methods=['GET'])
@auth.require(401)
@account_show_perm.require(403)
def show(account_id):
    user_data = User.query.get_or_404(account_id)
    return AccountSchema().jsonify(user_data)


@account_api.route('/accounts', methods=['GET'])
@auth.require(401)
@account_list_perm.require(403)
def index():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    role_id = request.args.get('role')
    users_query = User.query
    if role_id:
        users_query = users_query.filter(
            db.or_(
                User.primary_role_id == role_id,
                User.secondary_roles.any(id=role_id)))
    users = users_query.order_by(User.created_at.desc()).paginate(page, limit)

    return AccountSchema().jsonify(users)


@account_api.route('/accounts', methods=['POST'])
@auth.require(401)
@account_create_perm.require(403)
def create():
    payload = request.get_json()
    account_schema = AccountSchema(only=('name', 'email', 'password'))
    account_data, errors = account_schema.load(payload)
    if errors:
        return jsonify(code=20001, error=errors), 422
    account_data.save()
    return AccountSchema().jsonify(account_data)


@account_api.route('/accounts/<account_id>/password', methods=['PUT'])
@auth.require(401)
@account_update_perm.require(403)
def update_password(account_id):
    user_data = User.query.get_or_404(account_id)
    payload = request.get_json()
    password_data, errors = PasswordSchema().load(payload)
    if errors:
        return jsonify(code=20001, error=errors), 422
    user_data.password = password_data['new_password']
    user_data.save()
    return jsonify(code=10000, message='success')


@account_api.route('/accounts/<account_id>', methods=['PUT'])
@auth.require(401)
@account_update_perm.require(403)
def update(account_id):
    user_data = User.query.get_or_404(account_id)
    payload = request.get_json()
    user_data, errors = AccountSchema().load(payload)
    if errors:
        return jsonify(code=20001, error=errors), 422
    user_data.save()
    return AccountSchema().jsonify(user_data)


@account_api.route('/accounts/<account_id>', methods=['DELETE'])
@auth.require(401)
@account_destory_perm.require(403)
def destory(account_id):
    user_data = User.query.get_or_404(account_id)
    user_data.delete()

    return jsonify(code=10000, message='success')
