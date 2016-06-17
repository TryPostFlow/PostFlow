#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
import os
import json
from werkzeug.utils import import_string, find_modules
from flask import Flask, request, Blueprint, g, Response, abort
from flask_principal import identity_loaded, Identity

from .account.models import User
from .auth.models import Token
import extensions
from extensions import principals


def create_app(config=None, packages=None):
    app = Flask(
        __name__.split('.')[0],
        instance_path=os.getcwd(),
        instance_relative_config=True)

    if config is not None:
        app.config.from_pyfile(config)
    elif os.getenv('FLASK_ENV') == 'dev':
        app.config.from_pyfile('config/development.conf')
        app.logger.info("Config: Development")
    elif os.getenv('FLASK_ENV') == 'test':
        app.config.from_pyfile('config/test.conf')
        app.logger.info("Config: Test")
    else:
        app.config.from_pyfile('config/production.conf')
        app.logger.info("Config: Production")

    configure_extensions(app)
    configure_errorhandlers(app)
    configure_before_handlers(app)
    configure_after_handlers(app)
    configure_identity(app)
    # register blueprints
    configure_packages(app, packages)
    return app


def configure_extensions(app):
    for extension_name in extensions.__all__:
        getattr(extensions, extension_name).init_app(app)


def configure_packages(app, packages):
    for package_name in packages:
        package_name = '%s.%s' % (app.import_name, package_name)
        modules = find_modules(package_name)
        for module in modules:
            __import__(module)

        package = import_string(package_name)
        for attr_name in dir(package):
            attr = getattr(package, attr_name)
            if isinstance(attr, Blueprint):
                app.register_blueprint(attr)


def configure_identity(app):

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
        return Identity(token.user_id, 'Bearer')

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.user = User.query.from_identity(identity)


def configure_before_handlers(app):

    @app.before_request
    def check_post_data():
        if request.is_json and\
                request.method in ['POST', 'PUT'] and\
                not request.get_json():
            abort(400)

    @app.before_request
    def authenticate():
        g.user = getattr(g.identity, 'user', None)


def configure_after_handlers(self):

    @self.after_request
    def headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = \
            'PUT, GET, POST, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = (
            "Authorization,Content-Type,Accept,Origin,User-Agent,"
            "DNT,Cache-Control,X-Mx-ReqToken,Keep-Alive,"
            "X-Requested-With,If-Modified-Since, X-Total, X-Page")
        response.headers['Access-Control-Expose-Headers'] = \
            'X-Total, X-Page'

        if request.is_json:
            response.headers['Content-Type'] = 'application/json'
        return response


def configure_errorhandlers(app):

    @app.errorhandler(400)
    def empty_body(error):
        message = {
            'code': 400,
            'error': 'No input data provided'}
        return Response(
            response=json.dumps(message), status=400)

    @app.errorhandler(401)
    def unauthorized(error):
        message = {
            'code': 401,
            'error': 'Login required'}
        return Response(
            response=json.dumps(message), status=401)

    @app.errorhandler(403)
    def forbidden(error):
        message = {
            'code': 403,
            'error': 'Sorry, page not allowed'}
        return Response(
            response=json.dumps(message), status=403)

    @app.errorhandler(404)
    def page_not_found(error):
        message = {
            'code': 404,
            'error': 'Not Found: ' + request.url}
        return Response(
            response=json.dumps(message), status=404)

    @app.errorhandler(500)
    def server_error(error):
        message = {
            'code': 500,
            'error': 'Sorry, an error has occurred'}
        return Response(
            response=json.dumps(message), status=500)
