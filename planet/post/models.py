#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mistune

from datetime import datetime
from werkzeug import cached_property
from sqlalchemy.ext.hybrid import hybrid_property

from ..extensions import db


def get_all_posts(page, limit=20):
    return Post.query.order_by(Post.updated_at.desc()).paginate(page, limit)


def get_post(id_or_slug):
    return Post.query.filter(
        db.or_(Post.id == id_or_slug, Post.slug == id_or_slug)).first_or_404()


post_tag = db.Table(
    'post_tag',
    db.Column('post_id', db.Integer(), index=True),
    db.Column('tag_id', db.Integer(), index=True))


class Post(db.Model):

    STATUS_DRAFT = 0
    STATUS_PUBLIC = 1
    STATUS_REMOVED = 2

    STATUSES = {
        STATUS_DRAFT: 'draft',
        STATUS_PUBLIC: 'public',
        STATUS_REMOVED: 'closed'
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    markdown = db.Column(db.Text)
    _status = db.Column('status', db.SmallInteger, default=STATUS_DRAFT)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    tags = db.relationship(
        'Tag',
        secondary=post_tag,
        primaryjoin='Post.id == post_tag.c.post_id',
        secondaryjoin='post_tag.c.tag_id==Tag.id',
        foreign_keys='[post_tag.c.post_id, post_tag.c.tag_id]',
        backref='posts')

    user = db.relationship(
        'User',
        primaryjoin='Post.user_id == User.id',
        foreign_keys='Post.user_id',
        backref='posts')

    @cached_property
    def content(self):
        return mistune.markdown(self.markdown)

    @property
    def status(self):
        return self.STATUSES.get(self._status)
