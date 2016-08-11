#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, g

from . import api
from ..extensions import db
from ..schema import render_schema, render_error
from .schemas import PostSchema
from .models import get_all_posts, get_post
from ..permissions import auth
from .permissions import (post_create_perm,
                          post_update_perm, post_destory_perm)


@api.route('', methods=['GET'])
def index():
    page = int(request.values.get('p', 1))
    limit = int(request.values.get('limit', 20))
    posts = get_all_posts(page=page, limit=limit)
    return render_schema(posts, PostSchema)


@api.route('/<id_or_slug>', methods=['GET'])
def show(id_or_slug):
    post = get_post(id_or_slug)
    return render_schema(post, PostSchema)


@api.route('', methods=['POST'])
@auth.require(401)
@post_create_perm.require(403)
def create():
    payload = request.get_json()
    if not payload:
        return render_error(20001, 'No input data provided')
    post_schema = PostSchema(exclude=('id', 'created_at', 'updated_at'))
    post_data, errors = post_schema.load(payload)
    if errors:
        return render_error(20001, errors, 422)
    post_data.author = g.user
    post_data.updated_by = g.user.id
    db.session.add(post_data)
    db.session.commit()
    return render_schema(post_data, PostSchema)


@api.route('/<id>', methods=['PUT'])
@auth.require(401)
@post_update_perm.require(403)
def update(id):
    playload = request.get_json()
    if not playload:
        return render_error(20001, 'No input data provided')
    post_schema = PostSchema(exclude=('created_at', 'updated_at', 'author'))
    post, errors = post_schema.load(playload)
    if errors:
        return render_error(20001, errors, 422)
    post.updated_by = g.user.id
    db.session.add(post)
    db.session.commit()
    return render_schema(post, PostSchema)


@api.route('/<id>', methods=['DELETE'])
@auth.require(401)
@post_destory_perm.require(403)
def destory(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()

    message = {
        'code': 10000,
        'message': 'success'
    }

    return render_schema(message)
