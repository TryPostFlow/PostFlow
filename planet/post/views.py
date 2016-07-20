# -*- coding: utf-8 -*-

from . import post_view
from .models import get_all_posts, get_post, get_next_post, get_prev_post

from ..helpers.template import render_template


@post_view.route('/', methods=['GET'])
@post_view.route('/page/<int:page>', methods=['GET'])
def index(page=1):
    posts = get_all_posts(page)
    return render_template('index.html', posts=posts)


@post_view.route('/<path:slug>', methods=['GET'])
def show(slug):
    post = get_post(slug)
    next_post = get_next_post(post.id)
    prev_post = get_prev_post(post.id)
    return render_template(
        'post.html', post=post, next_post=next_post, prev_post=prev_post)
