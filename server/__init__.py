#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from werkzeug.utils import import_string, find_modules
from flask import Flask, request, Blueprint, g, current_app
from flask_principal import identity_loaded, Identity

from .schema import render_error
from .account.models import User
from .auth.models import Token
import extensions
from extensions import principals

packages = [
    'account',
    'auth',
    'post',
    'tag'
]


class App(Flask):
    """Custom Flask Class."""

    def __init__(
            self,
            import_name=__name__.split('.')[0],
            config=None,
            packages=None,
            extensions=None):
        super(App, self).__init__(
            import_name,
            instance_path=os.getcwd(),
            instance_relative_config=True)
        # config
        if os.getenv('FLASK') == 'dev':
            self.config.from_pyfile('config/development.conf')
            self.logger.info("Config: Development")
        elif os.getenv('FLASK') == 'test':
            self.config.from_pyfile('config/test.conf')
            self.logger.info("Config: Test")
        else:
            self.config.from_pyfile('config/production.conf')
            self.logger.info("Config: Production")

        self.configure_extensions(extensions)
        self.configure_errorhandlers()
        self.configure_before_handlers()
        self.configure_after_handlers()
        self.configure_identity()

        # register module
        self.configure_packages(packages)

    def configure_extensions(self, extensions):
        for extension_name in extensions.__all__:
            getattr(extensions, extension_name).init_app(self)

    def configure_packages(self, packages):
        for package_name in packages:
            package_name = '%s.%s' % (self.import_name, package_name)
            modules = find_modules(package_name)
            for module in modules:
                __import__(module)

            package = import_string(package_name)
            for attr_name in dir(package):
                attr = getattr(package, attr_name)
                if isinstance(attr, Blueprint):
                    self.register_blueprint(attr)

    def configure_identity(self):

        @principals.identity_loader
        def load_identity_from_header():
            header = request.headers.get('Authorization')
            if not header:
                return
            access_token = header.replace('Bearer ', '', 1)
            if not access_token:
                return
            token = Token.query.filter(
                Token.access_token == access_token).first()

            if not token:
                return
            # if token.is_expired:
            #     token.delete()
            #     return
            current_app.logger.info(token.user_id)
            return Identity(token.user_id, 'Bearer')

        @identity_loaded.connect_via(self)
        def on_identity_loaded(sender, identity):
            g.user = User.query.from_identity(identity)

    def configure_before_handlers(self):

        @self.before_request
        def authenticate():
            g.user = getattr(g.identity, 'user', None)

        # @self.before_request
        # def check_post_data():
        #     if request.method in ['POST', 'PUT'] and not request.get_json():
        #         abort(400)

    def configure_after_handlers(self):

        @self.after_request
        def headers(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = \
                'PUT, GET, POST, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = \
                'Authorization,Content-Type,Accept,Origin,User-Agent,\
                DNT,Cache-Control,X-Mx-ReqToken,Keep-Alive,X-Requested-With,\
                If-Modified-Since, X-Total, X-Page'
            response.headers['Content-Type'] = 'application/json'
            return response

    def configure_errorhandlers(self):

        @self.errorhandler(400)
        def empty_body(error):
            return render_error(400, 'No input data provided', 400)

        @self.errorhandler(401)
        def unauthorized(error):
            return render_error(401, 'Login required', 401)

        @self.errorhandler(402)
        def authorize_failed(error):
            return render_error(402, 'Authentication Failed', 402)

        @self.errorhandler(403)
        def forbidden(error):
            return render_error(403, 'Sorry, page not allowed', 403)

        @self.errorhandler(404)
        def page_not_found(error):
            return render_error(404, 'Not Found: ' + request.url, 404)

        @self.errorhandler(500)
        def server_error(error):
            return render_error(500, 'Sorry, an error has occurred', 500)

app = App(packages=packages, extensions=extensions)
