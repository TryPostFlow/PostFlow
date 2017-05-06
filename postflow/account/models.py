#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime
from werkzeug.utils import cached_property
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import BaseQuery
from flask_principal import RoleNeed, UserNeed

from postflow.extensions import db
from postflow.utils.database import CRUDMixin
from postflow.utils.permissions import Need
from postflow.helpers.text import slugify
from postflow.post.models import Post
from postflow.setting.models import get_setting


def auth_user(email, password):
    user = User.query.filter(User.email == email).first()
    authenticated = user.check_password(password) if user else False
    return user, authenticated


def get_all_users(page, limit=20):
    return User.query.order_by(User.updated_at.desc()).paginate(page, limit)


def get_posts_by_user(user_id, page, limit=None):
    limit = limit if limit else int(get_setting('postsPerPage').value)
    return Post.query.filter(Post.created_by == user_id).paginate(page, limit)


def create_user(name, password, email, role_name):
    role = Role.query.filter(Role.slug == role_name).first()
    if not role:
        role = Role.query.filter(Role.slug == 'admin').first()
    user = User.create(
        name=name, email=email, password=password, primary_role=role)
    return user


def update_user(name, password, email, role_name):
    """Update an existing user.
    Returns the updated user.

    :param name: The name of the user.
    :param password: The password of the user.
    :param email: The email address of the user.
    :param role_name: The name of the role to which the user
                      should belong to.
    """
    user = User.query.filter_by(name=name).first()
    if user is None:
        return None

    role = Role.query.filter(Role.slug == role_name).first()
    if not role:
        role = Role.query.filter(Role.slug == 'admin').first()

    user.password = password
    user.email = email
    user.primary_role = role
    return user.save()


user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer, index=True),
                     db.Column('role_id', db.Integer, index=True))

role_permission = db.Table('role_permission',
                           db.Column('role_id', db.Integer, index=True),
                           db.Column('permission_id', db.Integer, index=True))


class UserQuery(BaseQuery):
    def from_identity(self, identity):
        """
        Loads user from flaskext.principal.Identity instance and
        assigns permissions from user.
        A "user" instance is monkeypatched to the identity instance.
        If no user found then None is returned.
        """

        try:
            user = self.get(int(identity.id))
        except ValueError:
            user = None

        if user:
            identity.provides.update(user.provides)

        identity.user = user

        return user


class User(db.Model, CRUDMixin):
    query_class = UserQuery

    STATUS_ACTIVE = 'active'
    STATUS_FORBIDDEN = 'forbidden'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column('name', db.String(100), unique=True, index=True)
    _slug = db.Column('slug', db.String(100), unique=True, index=True)
    _password = db.Column("password", db.String(60), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    primary_role_id = db.Column(db.Integer)
    status = db.Column(db.String(100), nullable=False, default=STATUS_ACTIVE)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    primary_role = db.relationship(
        'Role',
        lazy="joined",
        backref="primary_users",
        uselist=False,
        primaryjoin='User.primary_role_id==Role.id',
        foreign_keys=[primary_role_id])

    secondary_roles = db.relationship(
        'Role',
        backref=db.backref('users', lazy='dynamic'),
        secondary=user_role,
        primaryjoin='User.id==user_role.c.user_id',
        secondaryjoin='user_role.c.role_id==Role.id',
        foreign_keys=[user_role.c.user_id, user_role.c.role_id],
        lazy='dynamic')

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name.strip()
        if self.slug is None:
            self.slug = slugify(name)[:255]

    @hybrid_property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, slug):
        self._slug = slugify(slug) if slug else slugify(self.name)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def roles(self):
        return [self.primary_role] + list(self.secondary_roles)

    @cached_property
    def permissions(self):
        perms = []
        for role in self.roles:
            perms.extend(role.permissions)
        role = Role.query.filter_by(slug='owner').first()
        if role and self.primary_role == role:
            perms.extend(Permission.query.all())
        return list(set(perms))

    @cached_property
    def provides(self):
        needs = [RoleNeed('authenticated'), UserNeed(self.id)]

        needs.extend([
            Need(perm.object_type, perm.action_type, perm.object_id)
            for perm in self.permissions
        ])

        return needs

    @cached_property
    def avatar(self):
        gravatar_url = "https://www.gravatar.com/avatar/"
        return gravatar_url + hashlib.md5(self.email.lower()).hexdigest()


def get_all_roles(page, limit=20):
    return Role.query.order_by(Role.created_at.desc()).paginate(page, limit)


def get_role(id_or_slug):
    return Role.query.filter(
        db.or_(Role.id == id_or_slug, Role.slug == id_or_slug)).first()


class Role(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    permissions = db.relationship(
        'Permission',
        backref='roles',
        secondary=role_permission,
        primaryjoin='Role.id==role_permission.c.role_id',
        secondaryjoin='role_permission.c.permission_id==Permission.id',
        foreign_keys=[
            role_permission.c.role_id, role_permission.c.permission_id
        ])


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    object_type = db.Column(db.String(150))
    action_name = db.Column(db.String(150))
    action_type = db.Column(db.String(150))
    object_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
