#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator
from flask_principal import RoleNeed, Permission


class Need(tuple):
    needs = []

    def __new__(self,
                method,
                value=None,
                object_id=None,
                method_name=None,
                value_name=None):
        self.needs.append(
            tuple.__new__(Need, (method, value, object_id, method_name,
                                 value_name)))
        return tuple.__new__(Need, (method, value, object_id, method_name,
                                    value_name))

    def __repr__(self):
        return 'Need(method={}, value={}, object_id={})'.format(
            self.method, self.value, self.object_id)

    def __eq__(self, other):
        return self.method == other.method and self.value == other.value\
            and self.object_id == other.object_id

    def __hash__(self):
        return hash((self.method, self.value, self.object_id))

    method = property(operator.itemgetter(0))
    value = property(operator.itemgetter(1))
    object_id = property(operator.itemgetter(2))
    method_name = property(operator.itemgetter(3))
    value_name = property(operator.itemgetter(4))


auth = Permission(RoleNeed('authenticated'))
