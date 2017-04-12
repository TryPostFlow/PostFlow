#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, current_app, url_for
from postflow.utils.schema import render_error
from postflow.oauth.models import Client
from postflow.auth import auth_api
from postflow.auth.schemas import LoginSchema


@auth_api.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    login_data, errors = LoginSchema().load(payload)
    if errors:
        return render_error(20001, errors, 422)
    client = Client.query.filter(Client.name == 'postflow').first()
    if not client:
        return render_error(30001, 'need client', 503)
    data = {
        'grant_type': 'password',
        'client_id': client.client_id,
        'client_secret': client.client_secret,
        'username': login_data.email,
        'password': payload.get('password')
    }
    resp = current_app.test_client().post(
        url_for('oauth_api.token'), data=data)
    return resp
