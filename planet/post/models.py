#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import re
import itertools
from datetime import datetime

import mistune
from jinja2.utils import Markup
from sqlalchemy.ext.hybrid import hybrid_property
from planet.extensions import db
from planet.helpers.text import slugify
from planet.setting.models import get_setting
from planet.utils.database import CRUDMixin


def get_all_posts(status=None, page=1, limit=None):
    limit = limit if limit else int(get_setting('postsPerPage').value)
    query = Post.query
    if status:
        query = query.filter(Post.status == status)
    return query.paginate(page, limit)


def get_post(id_or_slug):
    return Post.query.filter(
        db.or_(Post.id == id_or_slug, Post.slug == id_or_slug)).first_or_404()


def get_next_post(id):
    return Post.query.order_by(Post.id.asc()).filter(Post.id > id).first()


def get_prev_post(id):
    return Post.query.order_by(Post.id.desc()).filter(Post.id < id).first()


def add_post_views(id, views=1):
    post = Post.query.get(id)
    if not post:
        return
    post.views = post.views + views
    db.session.add(post)
    db.session.commit()


def insert_sample_post():
    post = Post.create(
        title="Welcome to Planet",
        slug="welcome-to-planet",
        status=Post.STATUS_PUBLIC,
        created_by=1,
        updated_by=1,
        published_by=1,
        markdown=\
        """
You're live! Nice. We've put together a little post to introduce you to the Planet editor and get you started. You can manage your content by signing in to the admin area at `<your blog URL>/Planet/`. When you arrive, you can select this post from a list on the left and see a preview of it on the right. Click the little pencil icon at the top of the preview to edit this post and read the next section!

## Getting Started

Planet uses something called Markdown for writing. Essentially, it's a shorthand way to manage your post formatting as you write!

Writing in Markdown is really easy. In the left hand panel of Planet, you simply write as you normally would. Where appropriate, you can use *shortcuts* to **style** your content. For example, a list:

* Item number one
* Item number two
    * A nested item
* A final item

or with numbers!

1. Remember to buy some milk
2. Drink the milk
3. Tweet that I remembered to buy the milk, and drank it

### Links

Want to link to a source? No problem. If you paste in a URL, like http://Planet.org - it'll automatically be linked up. But if you want to customise your anchor text, you can do that too! Here's a link to [the Planet website](http://Planet.org). Neat.

### What about Images?

Images work too! Already know the URL of the image you want to include in your article? Simply paste it in like this to make it show up:

![The Planet Logo](https://Planet.org/images/Planet.png)

Not sure which image you want to use yet? That's ok too. Leave yourself a descriptive placeholder and keep writing. Come back later and drag and drop the image in to upload:

![A bowl of bananas]


### Quoting

Sometimes a link isn't enough, you want to quote someone on what they've said. Perhaps you've started using a new blogging platform and feel the sudden urge to share their slogan? A quote might be just the way to do it!

> Planet - Just a blogging platform

### Working with Code

Got a streak of geek? We've got you covered there, too. You can write inline `<code>` blocks really easily with back ticks. Want to show off something more comprehensive? 4 spaces of indentation gets you there.

    .awesome-thing {
        display: block;
        width: 100%;
    }

### Ready for a Break? 

Throw 3 or more dashes down on any new line and you've got yourself a fancy new divider. Aw yeah.

---

### Advanced Usage

There's one fantastic secret about Markdown. If you want, you can write plain old HTML and it'll still work! Very flexible.

<input type="text" placeholder="I'm an input field!" />

That should be enough to get you started. Have fun - and let us know what you think :)
        """)
    return post


post_tag = db.Table(
    'post_tag',
    db.Column('post_id', db.Integer(), index=True),
    db.Column('tag_id', db.Integer(), index=True))


class Post(db.Model, CRUDMixin):

    STATUS_DRAFT = 'draft'
    STATUS_PUBLIC = 'published'
    STATUS_REMOVED = 'removed'

    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column('title', db.String(255))
    _slug = db.Column('slug', db.String(255), unique=True)
    _markdown = db.Column('markdown', db.Text)
    content = db.Column(db.Text)
    excerpt = db.Column(db.Text)
    views = db.Column(db.Integer, default=0)
    status = db.Column(db.String(150), default=STATUS_DRAFT)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, index=True)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, index=True)
    published_at = db.Column(db.DateTime)
    published_by = db.Column(db.Integer, index=True)

    __mapper_args__ = {'order_by': id.desc()}

    tags = db.relationship(
        'Tag',
        secondary=post_tag,
        primaryjoin='Post.id == post_tag.c.post_id',
        secondaryjoin='post_tag.c.tag_id==Tag.id',
        foreign_keys='[post_tag.c.post_id, post_tag.c.tag_id]',
        backref='posts')

    author = db.relationship(
        'User',
        primaryjoin='Post.created_by == User.id',
        foreign_keys='Post.created_by',
        backref='posts')

    @hybrid_property
    def markdown(self):
        return self._markdown

    @markdown.setter
    def markdown(self, markdown):
        self._markdown = markdown
        renderer = mistune.Renderer(escape=False)
        markdown = mistune.Markdown(renderer=renderer)
        self.content = markdown(self._markdown)

    def get_excerpt(self, length=100):
        # return re.sub(r'<.*?>', '', (self.excerpt or self.content))[:length]
        return Markup(self.excerpt or self.content).striptags()[:length]

    @hybrid_property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title.strip()
        if self.slug is None:
            self.slug = slugify(title)[:255]

    @hybrid_property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, slug):
        slugify_slug = slugify(slug) if slug else slugify(self.title)
        if not self._slug:
            self._slug = slugify_slug
            for x in itertools.count(1):
                if not db.session.query(
                        db.exists().where(Post.slug == self._slug)).scalar():
                    break
                self._slug = "{}-{}".format(slugify_slug, x)
            return
        self._slug = slugify_slug
