#!/usr/bin/env python
# coding=utf-8

import multiprocessing

from flask_mail import Message
from postflow.extensions import mail


def processing_pool(f):
    def wrapper(*args, **kwargs):
        pool = multiprocessing.Pool(processes=4)
        pool.apply_async(f, (args, kwargs))
        pool.close()
        pool.join()
    return wrapper


def send_async_mail(msg):
    mail.send(msg)


def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    pool = multiprocessing.Pool(processes=4)
    pool.apply_async(send_async_mail, (msg, ))
    pool.close()
    pool.join()
