#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from postflow.extensions import db
from postflow.utils.database import CRUDMixin


def get_setting(key):
    return Setting.query.filter(
        db.or_(Setting.key == key, Setting.id == key)).first()


def get_all_settings():
    return Setting.query.all()


def save_setting(key, value):
    setting = Setting.query.filter(Setting.key == key).first()
    setting = setting if setting else Setting(key=key)
    setting.value = value
    setting.save()
    return setting


class Setting(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(150), nullable=False)
    value = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
