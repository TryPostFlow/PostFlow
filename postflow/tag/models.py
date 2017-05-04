#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from postflow.extensions import db, storage
from postflow.utils.database import CRUDMixin
from postflow.helpers.text import slugify
from postflow.post.models import Post
from postflow.setting.models import get_setting


def get_tag(id_or_slug):
    return Tag.query.filter(
        db.or_(Tag.id == id_or_slug, Tag.slug == id_or_slug)).first()


def get_posts_by_tag(id, page, limit=None):
    limit = limit if limit else int(get_setting('postsPerPage').value)
    posts = Post.query\
        .join(Post.tags).filter(Tag.id == id).paginate(page, limit)
    return posts


class Tag(db.Model, CRUDMixin):

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
    _slug = db.Column('slug', db.String(150), unique=True)
    description = db.Column(db.Text)
    _image = db.Column('image', db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __mapper_args__ = {'order_by': id.desc()}

    @hybrid_property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, slug):
        slugify_slug = slugify(slug) if slug else slugify(self.title)
        if not self._slug:
            self._slug = slugify_slug

            for x in itertools.count(1):
                if not db.session.query(
                        db.exists().where(Tag.slug == self._slug)).scalar():
                    break
                self._slug = "{}-{}".format(slugify_slug, x)
            return
        self._slug = slugify_slug

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name.strip()
        if self.slug is None:
            self.slug = slugify(name)[:255]

    @hybrid_property
    def num_posts(self):
        return len(self.posts)

    @hybrid_property
    def image(self):
        if self._image:
            return dict(url=storage.url(self._image), filename=self._image)
        return {}

    @image.setter
    def image(self, image=None):
        if image is None:
            image = {}
        self._image = image.get('filename')

    image = db.synonym("_image", descriptor=image)
