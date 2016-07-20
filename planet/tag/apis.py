#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from . import tag_api
from ..extensions import db
from ..schema import render_schema
from .schemas import TagSchema
from .models import Tag


@tag_api.route('', methods=['GET'])
def list():
    page = int(request.values.get('p', 1))
    limit = int(request.values.get('limit', 20))
    q = request.values.get('q')
    tags_query = Tag.query
    if q:
        tags_query = tags_query.filter(Tag.name.like('%' + q + '%'))
    tags = tags_query.paginate(page, limit)
    return render_schema(tags, TagSchema)
