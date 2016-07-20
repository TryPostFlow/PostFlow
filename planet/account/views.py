# -*- coding: utf-8 -*-

from . import account_view
from .models import get_posts_by_user, get_user

from ..helpers.template import render_template


@account_view.route('/author/<slug>', methods=['GET'])
@account_view.route('/author/<slug>/page/<int:page>', methods=['GET'])
def show(slug, page=1):
    user = get_user(slug)
    posts = get_posts_by_user(user.id, page)
    return render_template(
        'author.html', author=user, posts=posts)
