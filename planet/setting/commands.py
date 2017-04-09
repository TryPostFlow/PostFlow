from planet.extensions import db
from planet.setting.schemas import SettingSchema
from planet.setting.fixtures import DEFAULT_SETTINGS


def init_settings():
    for default_setting in DEFAULT_SETTINGS:
        setting_data = SettingSchema().load(default_setting).data
        db.session.add(setting_data)
    db.session.commit()
