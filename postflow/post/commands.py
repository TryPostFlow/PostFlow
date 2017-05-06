#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from postflow.extensions import db
from postflow.post.fixtures import SAMPLE_POST
from postflow.post.schemas import PostSchema
from postflow.account.models import Role, User


def insert_sample_post():
    user_data = User.query\
        .join(Role, Role.id == User.primary_role_id)\
        .filter(Role.slug == 'owner').first()
    if not user_data:
        user_data = User.query.first()
    if not user_data:
        return
    post_data = PostSchema().load(SAMPLE_POST).data
    post_data.published_at = datetime.utcnow()
    post_data.published_by = user_data.id
    post_data.created_by = user_data.id
    post_data.updated_by = user_data.id
    post_data.save()
    return post_data
