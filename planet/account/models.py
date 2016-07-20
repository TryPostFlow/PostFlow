#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from werkzeug import cached_property, security
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import BaseQuery
from flask_principal import RoleNeed, UserNeed

from ..extensions import db
from ..permissions import Need
from ..post.models import Post
from ..setting.models import get_setting


def auth_user(email, password):
    user = User.query.filter(User.email == email).first()
    # authenticated = user.check_password(password) if user else False
    return user, True if user else False


def get_all_users(page, limit=20):
    return User.query.order_by(User.updated_at.desc()).paginate(page, limit)


def get_user(id_or_slug):
    return User.query.filter(
        db.or_(User.id == id_or_slug, User.slug == id_or_slug)).first()


def get_posts_by_user(id, page, limit=None):
    limit = limit if limit else int(get_setting('postsPerPage').value)
    posts = Post.query.filter(Post.author_id == id).paginate(page, limit)
    return posts


def create_user(name, email, password):
    user = User(name, email, password)
    db.session.add(user)
    db.session.commit()
    return user


user_role = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, index=True),
    db.Column('role_id', db.Integer, index=True))

role_permission = db.Table(
    'role_permission',
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


class User(db.Model):
    query_class = UserQuery

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)
    slug = db.Column(db.String(100), unique=True, index=True)
    _password = db.Column("password", db.String(60), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(100), nullable=False, default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    roles = db.relationship(
        'Role',
        backref='users',
        secondary=user_role,
        primaryjoin='User.id==user_role.c.user_id',
        secondaryjoin='user_role.c.role_id==Role.id',
        foreign_keys=[user_role.c.user_id, user_role.c.role_id])

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = security.generate_password_hash(password)

    def check_password(self, password):
        return password == self._password
        # return security.check_password_hash(self._password, password)

    @cached_property
    def permissions(self):
        perms = []
        for role in self.roles:
            perms.extend(role.permissions)
        return list(set(perms))

    @cached_property
    def provides(self):
        needs = [RoleNeed('authenticated'),
                 UserNeed(self.id)]

        needs.extend([
            Need(perm.object_type, perm.action_type, perm.object_id)
            for perm in self.permissions])

        return needs


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)
    permissions = db.relationship(
        'Permission',
        backref='roles',
        secondary=role_permission,
        primaryjoin='Role.id==role_permission.c.role_id',
        secondaryjoin='role_permission.c.permission_id==Permission.id',
        foreign_keys=[
            role_permission.c.role_id,
            role_permission.c.permission_id])


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    object_type = db.Column(db.String(150))
    action_type = db.Column(db.String(150))
    object_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)
