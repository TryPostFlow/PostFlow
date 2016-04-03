#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager, Shell

from werkzeug.contrib.fixers import ProxyFix
from server import app

from server.commands import CreateDBCommand, DropDBCommand,\
    _make_context, CreateSuperUserCommand, RegisterActionsCommand

from flask.ext.migrate import MigrateCommand

# from werkzeug.serving import run_simple
# from werkzeug.wsgi import DispatcherMiddleware

# def simple(env, resp):
#     resp(b'200 OK', [(b'Content-Type', b'text/plain')])
#     return [b'Hello WSGI World']


# app = DispatcherMiddleware(
#     simple,
#     {
#         '/api': api
#     }
# )

class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the 
    front-end server to add these headers, to let you quietly bind 
    this to a URL other than / and to an HTTP scheme that is 
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app.wsgi_app = ReverseProxied(app.wsgi_app)

manager = Manager(app)
manager.add_command('createdb', CreateDBCommand())
manager.add_command('dropdb', DropDBCommand())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('createsuperuser', CreateSuperUserCommand())
# manager.add_command('db', MigrateCommand)
manager.add_command('actions', RegisterActionsCommand)


if __name__ == '__main__':
    manager.run()
    # run_simple('localhost', 5000, app)
