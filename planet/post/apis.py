#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import request, g, jsonify, abort

from planet.extensions import db
from planet.utils.permissions import auth
from planet.utils.schema import render_schema, render_error
from planet.post import post_api
from planet.post.schemas import PostSchema
from planet.post.models import get_all_posts, get_post
from planet.post.permissions import (post_list_perm, post_show_perm,
                                     post_create_perm, post_update_perm,
                                     post_destory_perm)


@post_api.route('', methods=['GET'])
@auth.require(401)
@post_list_perm.require(403)
def index():
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 20))
    posts_data = get_all_posts(page=page, limit=limit)
    return PostSchema().jsonify(posts_data)


@post_api.route('/<post_id>', methods=['GET'])
@auth.require(401)
@post_show_perm.require(403)
def show(post_id):
    post_data = get_post(post_id)
    if not post_data:
        abort(404)
    return PostSchema().jsonify(post_data)


@post_api.route('', methods=['POST'])
@auth.require(401)
@post_create_perm.require(403)
def create():
    payload = request.get_json()
    post_data, errors = PostSchema().load(payload)
    if errors:
        return jsonify(code=20001, error=errors), 422
    post_data.author = g.user
    post_data.updated_by = g.user.id
    if post_data.status == 'published':
        post_data.published_at = datetime.utcnow
        post_data.published_by = g.user.id
    db.session.add(post_data)
    db.session.commit()
    return PostSchema().jsonify(post_data)


@post_api.route('/<post_id>', methods=['PUT'])
@auth.require(401)
@post_update_perm.require(403)
def update(post_id):
    post_data = get_post(post_id)
    if not post_data:
        abort(404)
    playload = request.get_json()
    post_data, errors = PostSchema().load(playload)
    if errors:
        return jsonify(code=20001, error=errors), 422
    post_data.updated_by = g.user.id
    if post_data.status != 'published' and playload.get(
            'status') == 'published':
        post_data.published_at = datetime.utcnow
        post_data.published_by = g.user.id
    db.session.add(post_data)
    db.session.commit()
    return PostSchema().jsonify(post_data)


@post_api.route('/<post_id>', methods=['DELETE'])
@auth.require(401)
@post_destory_perm.require(403)
def destory(post_id):
    post_data = get_post(post_id)
    if not post_data:
        abort(404)
    db.session.delete(post_data)
    db.session.commit()
    return jsonify(code=10000, message='success')
