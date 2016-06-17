#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from ..extensions import db


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
    name = db.Column(db.String(150))
    slug = db.Column(db.String(150))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)
