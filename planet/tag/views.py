# -*- coding: utf-8 -*-

from . import tag_view
from .models import get_posts_by_tag, get_tag

from ..helpers.template import render_template


@tag_view.route('/tag/<slug>', methods=['GET'])
def show(slug, page=1):
    tag = get_tag(slug)
    posts = get_posts_by_tag(tag.id, page)
    return render_template(
        'tag.html', tag=tag, posts=posts)
