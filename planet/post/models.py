#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import re
import mistune

from jinja2.utils import Markup

from datetime import datetime
from werkzeug import cached_property
from sqlalchemy.ext.hybrid import hybrid_property

from ..extensions import db
from ..setting.models import get_setting


def get_all_posts(page, limit=None):
    limit = limit if limit else int(get_setting('postsPerPage').value)
    return Post.query.order_by(Post.updated_at.desc()).paginate(page, limit)


def get_post(id_or_slug):
    return Post.query.filter(
        db.or_(Post.id == id_or_slug, Post.slug == id_or_slug)).first_or_404()


def get_next_post(id):
    return Post.query.order_by(Post.id.asc()).filter(Post.id > id).first()


def get_prev_post(id):
    return Post.query.order_by(Post.id.desc()).filter(Post.id < id).first()


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
    author_id = db.Column(db.Integer, index=True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    _markdown = db.Column('markdown', db.Text)
    content = db.Column(db.Text)
    excerpt = db.Column(db.Text)
    _status = db.Column('status', db.SmallInteger, default=STATUS_DRAFT)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    __mapper_args__ = {'order_by': id.desc()}

    tags = db.relationship(
        'Tag',
        secondary=post_tag,
        primaryjoin='Post.id == post_tag.c.post_id',
        secondaryjoin='post_tag.c.tag_id==Tag.id',
        foreign_keys='[post_tag.c.post_id, post_tag.c.tag_id]',
        backref='posts')

    author = db.relationship(
        'User',
        primaryjoin='Post.author_id == User.id',
        foreign_keys='Post.author_id',
        backref='posts')

    # @cached_property
    # def content(self):
    #     return mistune.markdown(self.markdown)
    @hybrid_property
    def markdown(self):
        return self._markdown

    @markdown.setter
    def markdown(self, markdown):
        self._markdown = markdown
        self.content = mistune.markdown(self._markdown)

    def get_excerpt(self, length=100):
        # return re.sub(r'<.*?>', '', (self.excerpt or self.content))[:length]
        return Markup(self.excerpt or self.content).striptags()[:length]

    @property
    def status(self):
        return self.STATUSES.get(self._status)
