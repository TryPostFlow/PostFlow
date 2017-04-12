# -*- coding: utf-8 -*-

from datetime import datetime

import click
import feedparser

from postflow.commands.base import postflow
from postflow.extensions import db
from postflow.post.models import Post
from postflow.tag.models import Tag

@postflow.group()
def importer():
    """Create, update or delete users."""
    pass


@importer.command('wordpress')
@click.option("--path", "-p",
              help="The configuration file to use for PostFlow.")
def wordpress(path):
    feed = feedparser.parse(path)
    for entry in feed.entries:
        post = Post()
        post.title = entry.title
        post.content = entry.content[0]['value']
        for tag_dict in entry.tags:
            tag = Tag.query.filter_by(name=tag_dict['term']).first()
            if not tag:
                tag = Tag(name=tag_dict['term'])
            post.tags.append(tag)

        published = datetime.strptime(entry.wp_post_date, '%Y-%m-%d %H:%M:%S')
        post.created_by = 1
        post.updated_by = 1
        post.published_by = 1
        post.slug = published.strftime('%Y/%m/'+entry.wp_post_id)
        post.created_at = published
        post.updated_at = published
        post.updated_at = published
        db.session.add(post)
        db.session.commit()
        click.secho("[+] {} created.".format(post.title), fg="cyan")
    click.secho("[+] The file has been successfully imported!",
                fg="green", bold=True)
