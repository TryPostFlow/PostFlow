#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from ..extensions import db
from ..post.models import Post
from ..setting.models import get_setting
from ..helpers.text import slugify


def get_tag(id_or_slug):
    return Tag.query.filter(
        db.or_(Tag.id == id_or_slug, Tag.slug == id_or_slug)).first()


def get_posts_by_tag(id, page, limit=None):
    limit = limit if limit else int(get_setting('postsPerPage').value)
    posts = Post.query\
        .join(Post.tags).filter(Tag.id == id).paginate(page, limit)
    return posts


class Tag(db.Model):

    STATUS_DRAFT = 0
    STATUS_PUBLIC = 1
    STATUS_REMOVED = 2

    STATUSES = {
        STATUS_DRAFT: 'draft',
        STATUS_PUBLIC: 'public',
        STATUS_REMOVED: 'closed'
    }

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column('name', db.String(150))
    slug = db.Column(db.String(150))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        if self.slug is None:
            self.slug = slugify(name)
