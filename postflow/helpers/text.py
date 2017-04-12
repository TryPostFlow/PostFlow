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
    text = text.decode() if isinstance(text, str) else text
    for item in lazy_pinyin(text):
        result = []
        for word in _punct_re.split(unidecode(item.lower())):
            word = word.decode() if isinstance(word, str) else word
            result.extend(unidecode(word).split())
        split_text.extend(result)
    return unicode(delim.join(split_text))

import tempfile
import itertools as IT
import os


def uniquify(path, sep=''):
    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s}{n:d}'.format(s=sep, n=next(count))
    orig = tempfile._name_sequence
    with tempfile._once_lock:
        tempfile._name_sequence = name_sequence()
        path = os.path.normpath(path)
        dirname, basename = os.path.split(path)
        filename, ext = os.path.splitext(basename)
        fd, filename = tempfile.mkstemp(
            dir=dirname, prefix=filename, suffix=ext)
        tempfile._name_sequence = orig
    os.unlink(filename)
    return filename
