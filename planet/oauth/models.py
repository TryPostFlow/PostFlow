#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from werkzeug.security import gen_salt
from sqlalchemy.ext.hybrid import hybrid_property
from planet.extensions import db
from planet.utils.database import CRUDMixin


def create_client(name):
    client = Client(
        name=name,
        client_id=gen_salt(40),
        client_secret=gen_salt(50),
        redirect_uris=[
            'http://localhost:8000/authorized',
            'http://127.0.0.1:8000/authorized',
            'http://127.0.1:8000/authorized',
            'http://127.1:8000/authorized',],
        default_scopes=['email', 'address',]
    )
    db.session.add(client)
    db.session.commit()
    return client


class Client(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    client_id = db.Column(db.String(40), index=True)
    client_secret = db.Column(db.String(55), unique=True, index=True,
                              nullable=False)
    _redirect_uris = db.Column('redirect_uris', db.Text)
    _default_scopes = db.Column('default_scopes', db.Text, default='email address')
    disallow_grant_type = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    @hybrid_property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @redirect_uris.setter
    def redirect_uris(self, redirect_uris):
        self._redirect_uris = ' '.join(redirect_uris)

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @hybrid_property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []

    @default_scopes.setter
    def default_scopes(self, default_scopes):
        self._default_scope = ' '.join(default_scopes)

    @property
    def allowed_grant_types(self):
        types = [
            'authorization_code', 'password',
            'client_credentials', 'refresh_token',
        ]
        if self.disallow_grant_type:
            types.remove(self.disallow_grant_type)
        return types


class Grant(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user = db.relationship(
        'User',
        primaryjoin='User.id == Grant.user_id',
        foreign_keys='Grant.user_id',
        cascade="all, delete-orphan")
    client_id = db.Column(db.String(40), nullable=False)
    client = db.relationship(
        'Client',
        primaryjoin='Client.client_id == Grant.client_id',
        foreign_keys='Grant.client_id',
        cascade="all, delete-orphan")
    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    _scopes = db.Column('scopes', db.Text)
    expires = db.Column(db.DateTime)


    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    @scopes.setter
    def scopes(self, scopes):
        self._scopes = ' '.join(scopes)


class Token(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(40), nullable=False)
    client = db.relationship(
        'Client',
        primaryjoin='Client.client_id == Token.client_id',
        foreign_keys='Token.client_id',
        cascade="all, delete-orphan")
    user_id = db.Column(db.Integer)
    user = db.relationship(
        'User',
        primaryjoin='User.id == Token.user_id',
        foreign_keys='Token.user_id',
        cascade="all, delete-orphan")
    user = db.relationship('User')
    client = db.relationship('Client')
    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    expires = db.Column(db.DateTime)
    _scopes = db.Column('scopes', db.Text)

    def __init__(self, **kwargs):
        expires_in = kwargs.pop('expires_in')
        self.expires = datetime.utcnow() + timedelta(seconds=expires_in)
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    @scopes.setter
    def scopes(self, scopes):
        self._scopes = ' '.join(scopes)

    @property
    def is_expired(self):
        return datetime.utcnow() > self.expires
