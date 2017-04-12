# -*- coding: utf-8 -*-

from collections import OrderedDict

DEFAULT_ROLES = OrderedDict(
    (
        ('owner', {
            'name': 'Owner',
            'slug': 'owner',
            'description': 'The Owner Role'
        }),
        ('admin', {
            'name': 'Administrator',
            'slug': 'admin',
            'description': 'The Administrator Role',
            'permissions': [
                {'object_type': 'account', 'action_type': 'list'},
                {'object_type': 'account', 'action_type': 'show'},
                {'object_type': 'account', 'action_type':'create'},
                {'object_type': 'account', 'action_type':'update'},
                {'object_type': 'account', 'action_type':'destory'},
                {'object_type': 'role', 'action_type': 'list'},
                {'object_type': 'role', 'action_type': 'show'},
                {'object_type': 'role', 'action_type':'create'},
                {'object_type': 'role', 'action_type':'update'},
                {'object_type': 'role', 'action_type':'destory'},
                {'object_type': 'image', 'action_type':'upload'},
                {'object_type': 'post', 'action_type': 'list'},
                {'object_type': 'post', 'action_type': 'show'},
                {'object_type': 'post', 'action_type':'create'},
                {'object_type': 'post', 'action_type':'update'},
                {'object_type': 'post', 'action_type':'destory'},
                {'object_type': 'tag', 'action_type': 'list'},
                {'object_type': 'tag', 'action_type': 'show'},
                {'object_type': 'tag', 'action_type':'create'},
                {'object_type': 'tag', 'action_type':'update'},
                {'object_type': 'tag', 'action_type':'destory'},
                {'object_type': 'setting', 'action_type': 'list'},
                {'object_type': 'setting', 'action_type': 'show'},
                {'object_type': 'setting', 'action_type':'update'},
            ]
        }),
        ('editor', {
            'name': 'Editor',
            'slug': 'editor',
            'description': 'The Editor role',
            'permissions': [
                {'object_type': 'image', 'action_type':'upload'},
                {'object_type': 'post', 'action_type': 'list'},
                {'object_type': 'post', 'action_type': 'show'},
                {'object_type': 'post', 'action_type':'create'},
                {'object_type': 'post', 'action_type':'update'},
                {'object_type': 'post', 'action_type':'destory'},
                {'object_type': 'tag', 'action_type': 'list'},
                {'object_type': 'tag', 'action_type': 'show'},
                {'object_type': 'tag', 'action_type':'create'},
                {'object_type': 'tag', 'action_type':'update'},
                {'object_type': 'tag', 'action_type':'destory'},
            ]
        }),
        ('Author', {
            'name': 'Author',
            'slug': 'author',
            'description': 'The Author role',
            'permissions': [
                {'object_type': 'image', 'action_type':'upload'},
                {'object_type': 'post', 'action_type': 'list'},
                {'object_type': 'post', 'action_type': 'show'},
                {'object_type': 'post', 'action_type':'create'},
                {'object_type': 'post', 'action_type':'update'},
                {'object_type': 'post', 'action_type':'destory'},
                {'object_type': 'tag', 'action_type': 'list'},
                {'object_type': 'tag', 'action_type': 'show'},
                {'object_type': 'tag', 'action_type':'create'},
                {'object_type': 'tag', 'action_type':'update'},
                {'object_type': 'tag', 'action_type':'destory'},
            ]
        })
    )
)
