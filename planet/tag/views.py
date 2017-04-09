# -*- coding: utf-8 -*-

from flask import abort
from planet.helpers.template import render_template
from planet.tag import tag_view
from planet.tag.models import get_posts_by_tag, get_tag


@tag_view.route('/tag/<slug>', methods=['GET'])
def show(slug, page=1):
    tag = get_tag(slug)
    if not tag:
        abort(404)
    posts = get_posts_by_tag(tag.id, page)
    return render_template('tag.html', tag=tag, posts=posts)
