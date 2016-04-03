#!/usr/bin/env python
# coding=utf-8

import re

from pypinyin import lazy_pinyin
from unidecode import unidecode

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
_pre_re = re.compile(r'<pre (?=l=[\'"]?\w+[\'"]?).*?>(?P<code>[\w\W]+?)</pre>')
_lang_re = re.compile(r'l=[\'"]?(?P<lang>\w+)[\'"]?')


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug. From http://flask.pocoo.org/snippets/5/"""
    split_text = []
    for item in lazy_pinyin(text):
        result = []
        for word in _punct_re.split(unidecode(item.lower())):
            result.extend(unidecode(word).split())
        split_text.extend(result)
    return unicode(delim.join(split_text))
