#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ujson as json
import flask_sqlalchemy
from marshmallow import Schema
from flask import Response


class BaseSchema(Schema):
    class Meta:
        additional = ("id", "created_at", "updated_at")
        dateformat = "%Y-%m-%dT%H:%M:%SZ"
        json_module = json


def render_schema(model, schema=None):
    headers = {}
    if schema is None:
        resp = json.dumps(model)
    elif isinstance(model, flask_sqlalchemy.Pagination):
        resp = schema(many=True).dumps(model.items).data
        headers['X-Total'] = model.total
        headers['X-Page'] = model.page
    elif isinstance(model, list):
        resp = schema(many=True).dumps(model).data
    else:
        resp = schema().dumps(model).data

    return Response(response=resp, headers=headers)


def render_error(code, error, status=400):
    message = {
        'code': code,
        'error': error}
    return Response(
        response=json.dumps(message), status=status)


def update_object(obj, data):
    for key, value in data.iteritems():
        setattr(obj, key, value)
    return obj
