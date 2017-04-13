#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
import os
import json
from collections import namedtuple
from werkzeug.utils import import_string, find_modules
from flask import Flask, request, Blueprint, g, Response, abort
from flask_principal import identity_loaded, Identity

from postflow import extensions
from postflow.extensions import principals, themes
from postflow.packages import PACKAGES
from postflow.helpers.template import render_template
from postflow.account.models import User
from postflow.oauth.models import Token
from postflow.setting.models import Setting


def create_app(config=None, packages=PACKAGES):
    app = Flask(
        __name__.split('.')[0],
        instance_path=os.getcwd(),
        instance_relative_config=True)

    plant_conf = os.path.join(app.instance_path, 'postflow.conf')
    default_conf = os.path.join(app.root_path, 'config/default.conf')
    if config:
        config = config
    elif os.path.exists(plant_conf):
        config = plant_conf
    else:
        config = default_conf

    app.config.from_pyfile(config)

    configure_extensions(app)
    configure_errorhandlers(app)
    configure_before_handlers(app)
    configure_after_handlers(app)
    configure_template_filters(app)
    configure_context_processors(app)
    configure_identity(app)
    # register blueprints
    configure_packages(app, packages)
    return app


def configure_extensions(app):
    themes.init_themes(
        app, app_identifier='postflow', theme_url_prefix='/content/themes')
    for extension_name in extensions.__all__:
        getattr(extensions, extension_name).init_app(app)


def configure_packages(app, packages):
    for package_name in packages:
        package_name = '%s.%s' % (app.import_name, package_name)
        modules = find_modules(package_name, include_packages=True)
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
        token = Token.query.filter(Token.access_token == access_token).first()

        if not token:
            return
        if token.is_expired:
            token.delete()
            return
        return Identity(token.user_id, 'Bearer')

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.user = User.query.from_identity(identity)


def configure_before_handlers(app):
    @app.before_request
    def authenticate():
        g.user = getattr(g.identity, 'user', None)

    @app.before_request
    def site():
        settings = Setting.query.all()
        settings_dict = {setting.key: setting.value for setting in settings}
        settings_dict['navigation'] = json.loads(settings_dict['navigation'])
        settings_dict['domain'] = request.url_root
        Site = namedtuple('Site', [setting for setting in settings_dict])
        g.site = Site(**settings_dict)


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
        message = {'code': 400, 'error': 'No input data provided'}
        return Response(response=json.dumps(message), status=400)

    @app.errorhandler(401)
    def unauthorized(error):
        message = {'code': 401, 'error': 'Login required'}
        return Response(response=json.dumps(message), status=401)

    @app.errorhandler(403)
    def forbidden(error):
        message = {'code': 403, 'error': 'Sorry, page not allowed'}
        return Response(response=json.dumps(message), status=403)

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_json:
            message = {'code': 404, 'error': 'Not Found: ' + request.url}
            return Response(response=json.dumps(message), status=404)
        return render_template('404.html', error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_json:
            message = {'code': 500, 'error': 'Sorry, an error has occurred'}
            return Response(response=json.dumps(message), status=500)
        return render_template('500.html', error=error)


def configure_template_filters(app):
    @app.template_filter()
    def format_datetime(datetime, format):
        return datetime.strftime(format)


def configure_context_processors(app):
    pass
    # @app.context_processor
    # def blog():
    #     settings = Setting.query.all()
    #     settings_dict = {setting.key: setting.value for setting in settings}
    #     settings_dict['navigation'] = json.loads(settings_dict['navigation'])
    #     settings_dict['domain'] = request.url_root
    #     Blog = namedtuple('Blog', [setting for setting in settings_dict])
    #     blog = Blog(**settings_dict)
    #     return dict(blog=blog)
