#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import setting
from .models import get_setting


@setting.route('', methods=['GET'])
def index():
    pass


@setting.route('/<id_or_key>', methods=['GET'])
def show(id_or_key):
    setting = get_setting(id_or_key)


@setting.route('/<id>', methods=['POST'])
def update(id):
    pass
