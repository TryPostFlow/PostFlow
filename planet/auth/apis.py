#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from flask import request, current_app, url_for
from . import auth_api
from .schemas import LoginSchema
from ..schema import render_error
from ..oauth.models import Client


@auth_api.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    if not payload:
        return render_error(20001, 'No input data provided')
    login_schema = LoginSchema()
    login_data, errors = login_schema.load(payload)
    if errors:
        return render_error(20001, errors, 422)
    client = Client.query.filter(Client.name == 'planet').first()
    if not client:
        return render_error(30001, 'need client', 503)
    data = {
        'grant_type': 'password',
        'client_id': client.client_id,
        'client_secret': client.client_secret,
        'username': login_data.email,
        'password': payload.get('password')
    }
    resp = current_app.test_client().post(url_for('oauth_api.token'), data=data)
    return resp
