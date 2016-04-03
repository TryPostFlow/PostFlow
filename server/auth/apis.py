#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from werkzeug.security import gen_salt
from flask import jsonify, g
from ..extensions import oauth, db

from . import api
from .models import Token, Client, Grant
from ..account.models import User


@oauth.clientgetter
def get_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def get_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.tokengetter
def get_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    if refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()
    return None


@oauth.grantsetter
def set_grant(client_id, code, request, *args, **kwargs):
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        scope=' '.join(request.scopes),
        user_id=g.user.id,
        expires=expires,
    )
    db.session.add(grant)
    db.session.commit()


@oauth.tokensetter
def set_token(token, request, *args, **kwargs):
    # In real project, a token is unique bound to user and client.
    # Which means, you don't need to create a token every time.
    tok = Token(**token)
    if request.response_type == 'token':
        tok.user_id = g.user.id
    else:
        tok.user_id = request.user.id
    tok.client_id = request.client.client_id
    db.session.add(tok)
    db.session.commit()


@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    # This is optional, if you don't need password credential
    # there is no need to implement this method
    user = User.query.filter(
        db.or_(
            User.name == username, User.email == username)).first()
    if user and user.check_password(password):
        return user
    return None


@api.route('/token', methods=['GET', 'POST'])
@oauth.token_handler
def token():
    return {}


@api.route('/client', methods=['POST'])
def client():
    client = Client(
        client_id=gen_salt(40),
        client_secret=gen_salt(50),
        _redirect_uris=' '.join([
            'http://localhost:8000/authorized',
            'http://127.0.0.1:8000/authorized',
            'http://127.0.1:8000/authorized',
            'http://127.1:8000/authorized',
            ])
    )
    db.session.add(client)
    db.session.commit()
    return jsonify(
        client_id=client.client_id,
        client_secret=client.client_secret,
    )
