#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify

from postflow.utils.permissions import auth
from postflow.account import role_api
from postflow.account.schemas import (RoleSchema, PermissionSchema,
                                      GroupPermissionSchema)
from postflow.account.models import (Role, Permission)
from postflow.account.permissions import (role_list_perm, role_show_perm,
                                          role_create_perm, role_update_perm,
                                          role_destory_perm)


@role_api.route('/roles', methods=['GET'])
@auth.require(401)
@role_list_perm.require(403)
def index():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    roles = Role.query.order_by(Role.created_at.desc()).paginate(page, limit)
    return RoleSchema(exclude=('permissions', )).jsonify(roles)


@role_api.route('/roles/<role_id>', methods=['GET'])
@auth.require(401)
@role_show_perm.require(403)
def show(role_id):
    role_data = Role.query.get_or_404(role_id)
    return RoleSchema().jsonify(role_data)


@role_api.route('/roles', methods=['POST'])
@auth.require(401)
@role_create_perm.require(403)
def create():
    payload = request.get_json()
    role_schema = RoleSchema(only=('name', 'description', 'permissions'))
    role_data, errors = role_schema.load(payload)
    if errors:
        return jsonify(code=20001, error=errors), 422
    role_data.save()
    return RoleSchema().jsonify(role_data)


@role_api.route('/roles/<role_id>', methods=['PUT'])
@auth.require(401)
@role_update_perm.require(403)
def update(role_id):
    role_data = Role.query.get_or_404(role_id)
    payload = request.get_json()
    role_data, errors = RoleSchema().load(payload)
    if errors:
        return jsonify(code=20001, error=errors), 422
    role_data.save()
    return RoleSchema().jsonify(role_data)


@role_api.route('/roles/<role_id>', methods=['DELETE'])
@auth.require(401)
@role_destory_perm.require(403)
def destory(role_id):
    role_data = Role.query.get_or_404(role_id)
    role_data.delete()

    return jsonify(code=10000, message='success')


@role_api.route('/permissions', methods=['GET'])
def permissions_index():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    format = request.args.get('format')
    if format == 'group':
        groups = Permission.query.group_by(Permission.object_type).all()
        group_permissions = []
        for group in groups:
            perms = Permission.query.filter(
                Permission.object_type == group.object_type).all()
            group_permissions.append({
                'name': group.name,
                'object_type': group.object_type,
                'permissions': perms
            })
        return GroupPermissionSchema().jsonify(group_permissions)
    permissions = Permission.query.order_by(
        Permission.created_at.desc()).paginate(page, limit)
    return PermissionSchema().jsonify(permissions)
