#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jwt
import calendar
import datetime
from flask import request, current_app, g

from . import api
from .schemas import AccountSchema, LoginSchema
from .models import get_user, get_all_users

from ..schema import render_schema, render_error
from ..extensions import db


# @api.route('/token', methods=['POST'])
# def token():
#     login_schema = LoginSchema(only=('email', 'password'))
#     account_data, errors = login_schema.load(request.get_json())
#     if errors:
#         return render_error(20001, errors, 422)

#     exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=86400)
#     payload = {
#         'id': account_data.id,
#         'name': account_data.name,
#         'email': account_data.email,
#         'exp': exp
#     }
#     token = jwt.encode(
#         payload,
#         current_app.config['SECRET_KEY'],
#         algorithm='HS256')
#     return render_schema(
#         {'token': token, 'exp': calendar.timegm(exp.timetuple())})


@api.route('/me', methods=['GET'])
def me():
    return render_schema(g.user, AccountSchema)


@api.route('/<int:id>', methods=['GET'])
def view(id):
    user = get_user(id)
    return render_schema(user, AccountSchema)


@api.route('', methods=['GET'])
def list():
    page = int(request.values.get('p', 1))
    limit = int(request.values.get('limit', 20))
    users = get_all_users(page, limit)
    return render_schema(users, AccountSchema)


@api.route('', methods=['POST'])
def create():
    payload = request.get_json()
    account_schema = AccountSchema(only=('name', 'email', 'password'))
    account_data, errors = account_schema.load(payload)
    if errors:
        return render_error(20001, errors, 422)
    db.session.add(account_data)
    db.session.commit()
    return render_schema(account_data, AccountSchema)


@api.route('/<int:id>', methods=['PUT'])
def edit():
    payload = request.get_json()
    account_schema = AccountSchema(only=('name', 'email', 'password'))
    account_data, errors = account_schema.load(payload).data
    if errors:
        return render_error(20001, errors, 422)
    db.session.add(account_data)
    db.session.commit()
    return render_schema(account_data, account_schema)
