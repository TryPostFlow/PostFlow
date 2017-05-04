from postflow.setting.schemas import SettingSchema
from postflow.setting.fixtures import DEFAULT_SETTINGS


def init_settings():
    for default_setting in DEFAULT_SETTINGS:
        setting_data = SettingSchema().load(default_setting).data
        setting_data.save()
