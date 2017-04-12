from postflow.extensions import db
from postflow.utils.permissions import Need
from postflow.account.models import Role, Permission
from postflow.account.schemas import RoleSchema
from postflow.account.fixtures import DEFAULT_ROLES


def init_permissions():
    for need in Need.needs:
        permission = Permission.query.filter(
            Permission.object_type == need.method,
            Permission.action_type == need.value).first()
        if not permission:
            permission = Permission(
                object_type=need.method, action_type=need.value)
            db.session.add(permission)
        permission.name = need.method_name
        permission.action_name = need.value_name
        db.session.add(permission)
    db.session.commit()

    for default_role in DEFAULT_ROLES:
        role_data = Role.query.filter_by(slug=default_role).first()
        if role_data:
            role_data = RoleSchema().load(DEFAULT_ROLES[default_role],
                                          role_data).data
        else:
            role_data = RoleSchema().load(DEFAULT_ROLES[default_role]).data
        db.session.add(role_data)
    db.session.commit()
