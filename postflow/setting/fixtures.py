import json

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
        'key': 'navigation',
        'value': json.dumps(DEFAULT_NAVIGATION)
    }
]
