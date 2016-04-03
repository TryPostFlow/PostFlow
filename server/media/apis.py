#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from . import api
from ..extensions import db
from ..beaker import render_schema, render_error
from .schemas import MediaSchema
from .models import get_all_medias, get_media


@api.route('', methods=['GET'])
def list():
    page = int(request.values.get('p', 1))
    limit = int(request.values.get('limit', 50))
    medias = get_all_medias(page, limit)
    return render_schema(medias, MediaSchema)


@api.route('/<int:id>', methods=['GET'])
def get(id):
    media = get_media(id)
    return render_schema(media, MediaSchema)
