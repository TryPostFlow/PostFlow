#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import flask_sqlalchemy
from marshmallow import SchemaOpts, Schema, post_load
from marshmallow.compat import iteritems
from flask import Response


class ModelSchemaOpts(SchemaOpts):
    """Options class for `BaseSchema`.
    Adds the following options:

    - ``model``: The SQLAlchemy model to generate the `Schema` from (required).
    """

    def __init__(self, meta):
        super(ModelSchemaOpts, self).__init__(meta)
        self.model = getattr(meta, 'model', None)


class BaseSchema(Schema):
    OPTIONS_CLASS = ModelSchemaOpts

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(BaseSchema, self).__init__(*args, **kwargs)
        self.context[
            'from'] = self.context.get('from') or self.__class__.__name__

    class Meta:
        # additional = ("id", "created_at", "updated_at")
        dateformat = "%Y-%m-%dT%H:%M:%SZ"

    def get_instance(self, data):
        """Retrieve an existing record by primary key(s)."""
        if not self.opts.model:
            return None
        props = get_primary_keys(self.opts.model)
        filters = {prop.key: data.get(prop.key) for prop in props}
        if None not in filters.values():
            return self.opts.model.query.filter_by(**filters).first()
        return None

    @post_load
    def make_instance(self, data):
        """Deserialize data to an instance of the model. Update an existing row
        if specified in `self.instance` or loaded by primary key(s) in the data;
        else create a new row.

        :param data: Data to deserialize.
        """
        instance = self.instance or self.get_instance(data)
        if not self.opts.model:
            return instance or data
        if instance is None:
            return self.opts.model(**data)
        if self.context['from'] == self.__class__.__name__:
            for key, value in iteritems(data):
                setattr(instance, key, value)
        return instance

    def load(self, data, instance=None, *args, **kwargs):
        """Deserialize data to internal representation.

        :param instance: Optional existing instance to modify.
        """
        self.instance = instance or self.instance
        ret = super(BaseSchema, self).load(data, *args, **kwargs)
        self.instance = None
        return ret

    def jsonify(self, obj):
        """Return a JSON response containing the serialized data.
        :param obj: Object to serialize.
        """
        headers = {}
        if isinstance(obj, flask_sqlalchemy.Pagination):
            resp = self.dumps(obj.items, many=True).data
            headers['X-Total'] = obj.total
            headers['X-Page'] = obj.page
        elif isinstance(obj, list):
            resp = self.dumps(obj, many=True).data
        else:
            resp = self.dumps(obj).data

        return Response(response=resp, headers=headers)


def get_primary_keys(model):
    """Get primary key properties for a SQLAlchemy model.
    :param model: SQLAlchemy model class
    """
    mapper = model.__mapper__
    return [
        mapper.get_property_by_column(column) for column in mapper.primary_key
    ]


def render_schema(model, schema=None):
    headers = {}
    if schema is None:
        resp = json.dumps(model)
    elif isinstance(model, flask_sqlalchemy.Pagination):
        schema.many = True
        resp = schema.dumps(model.items).data
        headers['X-Total'] = model.total
        headers['X-Page'] = model.page
    elif isinstance(model, list):
        schema.many = True
        resp = schema.dumps(model).data
    else:
        resp = schema.dumps(model).data

    return Response(response=resp, headers=headers)


def render_error(code, error, status=400):
    message = {'code': code, 'error': error}
    return Response(response=json.dumps(message), status=status)


def update_object(obj, data):
    for key, value in data.iteritems():
        print key, value
        setattr(obj, key, value)
    return obj
