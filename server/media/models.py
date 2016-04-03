#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from werkzeug import cached_property
from sqlalchemy.ext.hybrid import hybrid_property

from ..extensions import db


def get_all_medias(page, limit=20):
    return Media.query.order_by(Media.updated_at.desc()).paginate(page, limit)


def get_media(id):
    return Media.query.get_or_404(id)


class Media(db.Model):

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
    content = db.Column(db.Text)
    path = db.Column(db.String(255))
    _status = db.Column('status', db.SmallInteger, default=STATUS_DRAFT)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    @property
    def url(self):
        return self.path

    @property
    def status(self):
        return self.STATUSES.get(self._status)
