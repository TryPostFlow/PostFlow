#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator
from flask_principal import RoleNeed, Permission


class Need(tuple):
    needs = []

    def __new__(self, method, value=None, object_id=None):
        self.needs.append(tuple.__new__(Need, (method, value, object_id)))
        return tuple.__new__(Need, (method, value, object_id))

    def __repr__(self):
        return 'Need(method=%r, value=%r, object_id=%r)' % self

    method = property(operator.itemgetter(0))
    value = property(operator.itemgetter(1))
    object_id = property(operator.itemgetter(2))

auth = Permission(RoleNeed('authenticated'))
