#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from urllib import quote
from flask import g


def send_telegram_channel(message):
    if not g.site.telegram_token or not g.site.telegram_channel:
        return
    BOT_URL = "https://api.telegram.org/bot{bot_token}/".format(bot_token=g.site.telegram_token)
    send_url = "{bot_url}sendMessage?chat_id={chat_id}&text={message}".format(
        bot_url=BOT_URL, chat_id=g.site.telegram_channel, message=quote(message));
    resp = requests.get(send_url)
    return resp.json()
