# -*- coding: utf-8 -*-

from flask import g, request, url_for, jsonify
from werkzeug.contrib.atom import AtomFeed
from postflow.extensions import db
from postflow.helpers.template import render_template
from postflow.post import post_view
from postflow.post.models import (get_all_posts, get_next_post, get_prev_post,
                                  Post)


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
        generator=('PostFlow', '', '0.1'))
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
    post_data = Post.query.filter(
        db.or_(Post.id == slug, Post.slug == slug)).first_or_404()
    post_data.views += 1
    post_data.save()
    return jsonify(code=10000, message='success')


@post_view.route('/<path:slug>', methods=['GET'])
def show(slug):
    post_data = Post.query.filter(
        db.or_(Post.id == slug, Post.slug == slug)).first_or_404()
    next_post = get_next_post(post_data.id)
    prev_post = get_prev_post(post_data.id)
    return render_template(
        'post.html', post=post_data, next_post=next_post, prev_post=prev_post)
