#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, g

from planet.extensions import db
from planet.utils.schema import render_schema, render_error
from planet.utils.permissions import auth
from planet.account import role_api
from planet.account.schemas import RoleSchema, PermissionSchema, GroupPermissionSchema
from planet.account.models import (get_role, get_all_roles, Permission)
from planet.account.permissions import (role_list_perm, role_show_perm,
                                        role_create_perm, role_update_perm,
                                        role_destory_perm)


@role_api.route('/roles', methods=['GET'])
@auth.require(401)
@role_list_perm.require(403)
def index():
    page = int(request.values.get('page', 1))
    limit = int(request.values.get('limit', 20))
    roles = get_all_roles(page, limit)
    return render_schema(roles, RoleSchema)


@role_api.route('/roles/<id_or_slug>', methods=['GET'])
@auth.require(401)
@role_show_perm.require(403)
def show(id_or_slug):
    role = get_role(id_or_slug)
    return render_schema(role, RoleSchema)


@role_api.route('/roles', methods=['POST'])
@auth.require(401)
@role_create_perm.require(403)
def create():
    payload = request.get_json()
    role_schema = RoleSchema(only=('name', 'description'))
    role_data, errors = role_schema.load(payload)
    if errors:
        return render_error(20001, errors, 422)
    db.session.add(role_data)
    db.session.commit()
    return render_schema(role_data, RoleSchema)


@role_api.route('/roles/<id>', methods=['PUT'])
@auth.require(401)
@role_update_perm.require(403)
def update(id):
    payload = request.get_json()
    role_schema = RoleSchema(only=('id', 'name', 'description', 'permissions'))
    role_data, errors = role_schema.load(payload)
    if errors:
        return render_error(20001, errors, 422)
    db.session.add(role_data)
    db.session.commit()
    return render_schema(role_data, RoleSchema)


@role_api.route('/roles/<id>', methods=['DELETE'])
@auth.require(401)
@role_destory_perm.require(403)
def destory(id):
    role = get_role(id)
    db.session.delete(role)
    db.session.commit()

    message = {'code': 10000, 'message': 'success'}

    return render_schema(message)


@role_api.route('/permissions', methods=['GET'])
def permissions_index():
    page = int(request.values.get('page', 1))
    limit = int(request.values.get('limit', 50))
    format = request.args.get('format')
    if format == 'group':
        groups = Permission.query.group_by(Permission.object_type).all()
        group_permissions = []
        for group in groups:
            perms = Permission.query.filter(
                Permission.object_type == group.object_type).all()
            group_permissions.append({
                'group': group.object_type,
                'permissions': perms
            })
        return render_schema(group_permissions, GroupPermissionSchema)
    permissions = Permission.query.order_by(
        Permission.created_at.desc()).paginate(page, limit)
    return render_schema(permissions, PermissionSchema)
