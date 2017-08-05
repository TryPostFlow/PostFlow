import json

from postflow.setting.schemas import SettingSchema

DEFAULT_NAVIGATION = [
    {
        "label": "Home",
        "url": "/"
    },
]

DEFAULT_SETTINGS = [
    # 'activeTheme': 'casper',
    {
        'key': 'title',
        'value': 'PostFlow'
    },
    {
        'key': 'description',
        'value': 'Thoughts, stories and ideas.'
    },
    {
        'key': 'logo',
        'value': '',
    },
    {
        'key': 'cover',
        'value': '',
    },
    {
        'key': 'postsPerPage',
        'value': '5',
    },
    {
        'key': 'disqus_id',
        'value': '',
    },
    {
        'key': 'ga_id',
        'value': '',
    },
    {
        'key': 'telegram_token',
        'value': ''
    },
    {
        'key': 'telegram_channel',
        'value': ''
    },
    {
        'key': 'navigation',
        'value': json.dumps(DEFAULT_NAVIGATION)
    }
]


def init_settings():
    for default_setting in DEFAULT_SETTINGS:
        setting_data = SettingSchema().load(default_setting).data
        setting_data.save()