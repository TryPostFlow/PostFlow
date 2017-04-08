#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify, abort
from planet.extensions import db
from planet.utils.permissions import auth
from planet.utils.schema import render_schema, render_error
from planet.tag import tag_api
from planet.tag.schemas import TagSchema
from planet.tag.models import Tag, get_tag
from planet.tag.permissions import (tag_list_perm, tag_show_perm,
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
    tag_data = get_tag(tag_id)
    if not tag_data:
        abort(404)
    return TagSchema().jsonify(tag_data)


@tag_api.route('', methods=['POST'])
@auth.require(401)
@tag_create_perm.require(403)
def create():
    payload = request.get_json()
    tag_data, errors = TagSchema(exclude=('id', )).load(payload)
    if errors:
        return jsonify(code=20001, error=errors), 422
    db.session.add(tag_data)
    db.session.commit()
    return TagSchema().jsonify(tag_data)


@tag_api.route('/<tag_id>', methods=['PUT'])
@auth.require(401)
@tag_update_perm.require(403)
def update(tag_id):
    payload = request.get_json()
    tag_data = get_tag(tag_id)
    if not tag_data:
        abort(404)
    tag_data, errors = TagSchema().load(payload)
    if errors:
        return render_error(20001, errors, 422)
    db.session.add(tag_data)
    db.session.commit()
    return TagSchema().jsonify(tag_data)


@tag_api.route('/<tag_id>', methods=['DELETE'])
@auth.require(401)
@tag_destory_perm.require(403)
def destory(tag_id):
    tag_data = get_tag(tag_id)
    if not tag_data:
        abort(404)
    db.session.delete(tag_data)
    db.session.commit()

    return jsonify(code=10000, message='success')
