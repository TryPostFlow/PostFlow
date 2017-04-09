#!/usr/bin/env python
# -*- coding: utf-8 -*-

from planet.extensions import db
from planet.post.fixtures import SAMPLE_POST
from planet.post.schemas import PostSchema


def insert_sample_post():
    post_data = PostSchema().load(SAMPLE_POST).data
    db.session.add(post_data)
    db.session.commit()
    return post_data
