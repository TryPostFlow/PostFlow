#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, abort

from . import api
from ..extensions import db
from ..schema import render_schema, render_error
from .schemas import PostSchema
from .models import get_all_posts, get_post
from .permissions import (post_index_perm, post_create_perm,
                          post_show_perm, post_update_perm, post_destory_perm)


@api.route('', methods=['GET'])
@post_index_perm.require()
def index():
    page = int(request.values.get('p', 1))
    limit = int(request.values.get('limit', 20))
    posts = get_all_posts(page, limit)
    return render_schema(posts, PostSchema)


@api.route('/<id_or_slug>', methods=['GET'])
def show(id_or_slug):
    post = get_post(id_or_slug)
    return render_schema(post, PostSchema)


@api.route('', methods=['POST'])
def create():
    payload = request.get_json()
    if not payload:
        return render_error(20001, 'No input data provided')
    post_schema = PostSchema(exclude=('id', 'created_at', 'updated_at'))
    post_data, errors = post_schema.load(payload)
    if errors:
        return render_error(20001, errors, 422)
    db.session.add(post_data)
    db.session.commit()
    return render_schema(post_data, PostSchema)


@api.route('/<id>', methods=['PUT'])
def update(id):
    payload = request.get_json()
    if not payload:
        return render_error(20001, 'No input data provided')
    post = get_post(id)
    post_schema = PostSchema(exclude=('created_at', 'updated_at'))
    post, errors = post_schema.load(payload)
    if errors:
        return render_error(20001, errors, 422)
    db.session.add(post)
    db.session.commit()
    return render_schema(post, PostSchema)


@api.route('/<id>', methods=['DELETE'])
def destory(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()

    message = {
        'code': 10000,
        'message': 'success'
    }

    return render_schema(message)
