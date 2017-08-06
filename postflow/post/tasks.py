#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from urllib import quote
from flask import g
from postflow.utils.async_func import run_async
from postflow.setting.models import get_setting

@run_async
def send_telegram_channel(message):
    telegram_token_setting = get_setting('telegram_token')
    telegram_channel_setting = get_setting('telegram_channel')
    if not telegram_token_setting or not telegram_channel_setting:
        return
    telegram_token = telegram_token_setting.value
    telegram_channel = telegram_channel_setting.value
    BOT_URL = "https://api.telegram.org/bot{bot_token}/".format(bot_token=telegram_token)
    send_url = "{bot_url}sendMessage?chat_id={chat_id}&text={message}".format(
        bot_url=BOT_URL, chat_id=telegram_channel, message=quote(message));
    resp = requests.get(send_url)
    return resp.json()
