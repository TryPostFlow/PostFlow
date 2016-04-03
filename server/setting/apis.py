#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import setting

@setting.route('', methods=['GET'])
def index():
    pass

@setting.route('/<id>', methods=['GET'])
def show(id):
    pass
