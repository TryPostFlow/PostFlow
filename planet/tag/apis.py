#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
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
    page = int(request.values.get('p', 1))
    limit = int(request.values.get('limit', 20))
    q = request.values.get('q')
    tags_query = Tag.query
    if q:
        tags_query = tags_query.filter(Tag.name.like('%' + q + '%'))
    tags = tags_query.paginate(page, limit)
    return render_schema(tags, TagSchema())


@tag_api.route('/<id_or_slug>', methods=['GET'])
@auth.require(401)
@tag_show_perm.require(403)
def show(id_or_slug):
    tag = get_tag(id_or_slug)
    return render_schema(tag, TagSchema())


@tag_api.route('', methods=['POST'])
@auth.require(401)
@tag_create_perm.require(403)
def create():
    payload = request.get_json()
    if not payload:
        return render_error(20001, 'No input data provided')
    tag_schema = TagSchema(exclude=('id', 'created_at', 'updated_at'))
    tag_data, errors = tag_schema.load(payload)
    if errors:
        return render_error(20001, errors, 422)
    db.session.add(tag_data)
    db.session.commit()
    return render_schema(tag_data, TagSchema())


@tag_api.route('/<id>', methods=['PUT'])
@auth.require(401)
@tag_update_perm.require(403)
def update(id):
    payload = request.get_json()
    if not payload:
        return render_error(20001, 'No input data provided')
    tag = get_tag(id)
    tag_schema = TagSchema(exclude=('image', 'num_posts', 'created_at',
                                    'updated_at'))
    tag, errors = tag_schema.load(payload)
    if errors:
        return render_error(20001, errors, 422)
    db.session.add(tag)
    db.session.commit()
    return render_schema(tag, TagSchema())


@tag_api.route('/<id>', methods=['DELETE'])
@auth.require(401)
@tag_destory_perm.require(403)
def destory(id):
    tag = get_tag(id)
    db.session.delete(tag)
    db.session.commit()

    message = {'code': 10000, 'message': 'success'}

    return render_schema(message)
