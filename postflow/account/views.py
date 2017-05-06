# -*- coding: utf-8 -*-

from flask import abort
from postflow.extensions import db
from postflow.account import account_view
from postflow.account.models import User
from postflow.account.models import get_posts_by_user

from postflow.helpers.template import render_template


@account_view.route('/author/<slug>', methods=['GET'])
@account_view.route('/author/<slug>/page/<int:page>', methods=['GET'])
def show(slug, page=1):
    user_data = User.query.filter(
        db.or_(User.id == slug, User.slug == slug)).first_or_404()
    posts = get_posts_by_user(user_data.id, page)
    return render_template('author.html', author=user_data, posts=posts)
