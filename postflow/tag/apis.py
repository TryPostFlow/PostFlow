#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify, abort
from postflow.extensions import db
from postflow.utils.permissions import auth
from postflow.tag import tag_api
from postflow.tag.schemas import TagSchema
from postflow.tag.models import Tag, get_tag
from postflow.tag.permissions import (tag_list_perm, tag_show_perm,
                                      tag_create_perm, tag_update_perm,
                                      tag_destory_perm)


@tag_api.route('', methods=['GET'])
@auth.require(401)
@tag_list_perm.require(403)
def list():
    page = int(request.args.get('p', 1))
    limit = int(request.args.get('limit', 20))
    query = request.args.get('q')
    tags_query = Tag.query
    if query:
        tags_query = tags_query.filter(Tag.name.like('%{}%'.format(query)))
    tags_data = tags_query.paginate(page, limit)
    return TagSchema().jsonify(tags_data)


@tag_api.route('/<tag_id>', methods=['GET'])
@auth.require(401)
@tag_show_perm.require(403)
def show(tag_id):
    tag_data = Tag.query.filter(
        db.or_(Tag.id == tag_id, Tag.slug == tag_id)).first_or_404()
    return TagSchema().jsonify(tag_data)


@tag_api.route('', methods=['POST'])
@auth.require(401)
@tag_create_perm.require(403)
def create():
    payload = request.get_json()
    tag_data, errors = TagSchema(exclude=('id', )).load(payload)
    if errors:
        return jsonify(code=20001, error=errors), 422
    tag_data.save()
    return TagSchema().jsonify(tag_data)


@tag_api.route('/<tag_id>', methods=['PUT'])
@auth.require(401)
@tag_update_perm.require(403)
def update(tag_id):
    payload = request.get_json()
    tag_data = Tag.query.filter(
        db.or_(Tag.id == tag_id, Tag.slug == tag_id)).first_or_404()
    tag_data, errors = TagSchema().load(payload)
    if errors:
        return jsonify(code=20001, error=errors), 422
    tag_data.save()
    return TagSchema().jsonify(tag_data)


@tag_api.route('/<tag_id>', methods=['DELETE'])
@auth.require(401)
@tag_destory_perm.require(403)
def destory(tag_id):
    tag_data = Tag.query.filter(
        db.or_(Tag.id == tag_id, Tag.slug == tag_id)).first_or_404()
    tag_data.delete()

    return jsonify(code=10000, message='success')
