# -*- coding: utf-8 -*-

from flask import g, request, url_for
from werkzeug.contrib.atom import AtomFeed
from . import post_view
from .models import (
    get_all_posts, get_post, get_next_post,
    get_prev_post, add_post_views, Post)

from ..schema import render_schema
from ..helpers.template import render_template


@post_view.route('/', methods=['GET'])
@post_view.route('/page/<int:page>', methods=['GET'])
def index(page=1):
    posts = get_all_posts(Post.STATUS_PUBLIC, page)
    return render_template('index.html', posts=posts)


@post_view.route('/feed')
def feed():
    feed = AtomFeed(
        g.site.title,
        feed_url=request.url,
        url=request.url_root,
        subtitle=g.site.description,
        generator=('Planet', '', '0.1'))
    posts = get_all_posts(Post.STATUS_PUBLIC)
    for post in posts.items:
        feed.add(
            post.title,
            post.get_excerpt(),
            content_type="html",
            author=post.author.name,
            url=url_for('post_view.show', slug=post.slug, _external=True),
            updated=post.updated_at,
            published=post.published_at)
    return feed.get_response()


@post_view.route('/<path:slug>/views', methods=['POST'])
def hit(slug):
    post = get_post(slug)
    add_post_views(post.id)
    message = {
        'code': 10000,
        'message': 'success'
    }
    return render_schema(message)


@post_view.route('/<path:slug>', methods=['GET'])
def show(slug):
    post = get_post(slug)
    next_post = get_next_post(post.id)
    prev_post = get_prev_post(post.id)
    return render_template(
        'post.html', post=post, next_post=next_post, prev_post=prev_post)
