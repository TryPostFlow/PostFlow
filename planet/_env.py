# coding:utf-8
import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


# import simplejson
# import json

# json.dump = simplejson.dump
# json.dumps = simplejson.dumps
# json.loads = simplejson.loads
# json.load = simplejson.load


# check the mimetype of request is json or not.
# this function will be added in Flask v0.11

@property
def is_json(self):
    """Indicates if this request is JSON or not.  By default a request
    is considered to include JSON data if the mimetype is
    :mimetype:`application/json` or :mimetype:`application/*+json`.
    .. versionadded:: 1.0
    """
    mt = self.mimetype or self.headers.get('Accept')
    if not mt:
        return False
    if 'application/json' in mt:
        return True
    if mt.startswith('application/') and mt.endswith('+json'):
        return True
    return False


from flask import Request

Request.is_json = is_json


import uuid
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value)
            else:
                # hexstring
                return "%.32x" % value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


from flask_sqlalchemy import SQLAlchemy


SQLAlchemy.GUID = GUID
