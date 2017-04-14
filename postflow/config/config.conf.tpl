TESTING = False

# Security
SECRET_KEY = "{{secret_key}}"

# Database
SQLALCHEMY_DATABASE_URI = '{{database_uri}}'
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_ECHO = False

# Theme
THEME_PATHS = ('{{theme_paths}}', )
THEME = '{{theme}}'

# Storage
STORAGE_TYPE='{{storage_type}}'
STORAGE_CONFIG={
    'base_url': '{{storage_base_url}}',
    'base_path': '{{storage_base_path}}',
    'base_dir': '{{storage_base_dir}}',
}

# SMTP Server
MAIL_SERVER = "{{ mail_server }}"
MAIL_PORT = {{ mail_port }}
MAIL_USE_SSL = {{ mail_use_ssl }}
MAIL_USE_TLS = {{ mail_use_tls }}
MAIL_USERNAME = "{{ mail_username }}"
MAIL_PASSWORD = "{{ mail_password }}"
MAIL_DEFAULT_SENDER = ("{{ mail_sender_name }}", "{{ mail_sender_address }}")
# Where to logger should send the emails to
ADMINS = ["{{ mail_admin_address }}"]

SENTRY_DSN = '{{sentry_dsn}}'

