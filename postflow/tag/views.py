# -*- coding: utf-8 -*-

from postflow.helpers.template import render_template
from postflow.extensions import db
from postflow.tag import tag_view
from postflow.tag.models import get_posts_by_tag, Tag


@tag_view.route('/tag/<slug>', methods=['GET'])
def show(slug, page=1):
    tag_data = Tag.query.filter(
        db.or_(Tag.id == slug, Tag.slug == slug)).first_or_404()
    posts = get_posts_by_tag(tag_data.id, page)
    return render_template('tag.html', tag=tag_data, posts=posts)
