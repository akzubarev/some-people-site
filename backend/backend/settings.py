import sys

"""
   _____  _______________  ________   __  _______
  /  _/ |/ / __/_  __/ _ |/ ___/ _ | /  |/  / __/
 _/ //    /\ \  / / / __ / (_ / __ |/ /|_/ / _/
/___/_/|_/___/ /_/ /_/ |_\___/_/ |_/_/  /_/___/
"""

import os

from dotenv import load_dotenv
from mixins.enums import Locale

load_dotenv()

# ___  _______  ____
# / _ \/  _/ _ \/ __/
# / // // // , _/\ \
# /____/___/_/|_/___/

SETTINGS_DIR = os.path.dirname((os.path.abspath(__file__)))

sys.path.append(SETTINGS_DIR)

USE_TZ = True
TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Moscow")
if not TIME_ZONE:
    TIME_ZONE = "Europe/Moscow"
BACKEND_DIR = os.path.dirname(SETTINGS_DIR)
BASE_DIR = BACKEND_DIR
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [("landings", os.path.join(BASE_DIR, "landings"))]
CKEDITOR_UPLOAD_PATH = MEDIA_ROOT + "/ckeditor"

LOCALE_PATHS = [os.path.join(BACKEND_DIR, "locale")]


# _______   ____  ___  ___   __   ____
# / ___/ /  / __ \/ _ )/ _ | / /  / __/
# / (_ / /__/ /_/ / _  / __ |/ /___\ \
# \___/____/\____/____/_/ |_/____/___/

SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
DEBUG = bool(int(os.getenv("DEBUG", "0")))

# ALLOWED_HOSTS = os.getenv("DOMAINS").split(",")
DOMAIN = 'somepeoplelarp.ru'
ALLOWED_HOSTS = ('*',)


CRYPT_KEY = b"JOPRHcd00KS9wQb_SaGwPyeyR-AMyfsclCWs_KJcLXk="
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_GROUP_CHATS = [
    {
        "language": "en",
        "id": "@pin2pay_en"
    },
    {
        "language": "ru",
        "id": "@pin2pay_ru"
    },
]

CSRF_COOKIE_SECURE = False

if os.getenv("CSRF_TRUSTED_ORIGINS"):
    CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split(",")

ROOT_URLCONF = "backend.urls"
AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'apps.users.views.login_email_username.EmailOrUsernameModelBackend',
)

# ______  ______   ______
# / __/  |/  / _ | /  _/ /
# / _// /|_/ / __ |_/ // /__
# /___/_/  /_/_/ |_/___/____/

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
email = 'mailgram'

if email == 'mailgram':
    CELERY_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    EMAIL_HOST = "box.mailgram.me"
    EMAIL_USE_SSL = True
    EMAIL_PORT = 465
    EMAIL_HOST_USER = "no-reply@pintopay.club"
    EMAIL_HOST_PASSWORD = "poxpik-1qaBci-dymmex"


DEFAULT_FROM_EMAIL = "Pin2Pay <no-reply@pintopay.club>"

# ___   ___  ___  ____
# / _ | / _ \/ _ \/ __/
# / __ |/ ___/ ___/\ \`
# /_/ |_/_/  /_/  /___/

INSTALLED_APPS = [
    # Django Admin

    'django_yarnpkg',
    'jazzmin',
    'admin_tools',
    'admin_tools.menu',
    'bulk_admin',
    'related_admin',
    "django.contrib.admin",
    "ordered_model",
    # Django modules
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    # "django.contrib.sites",
    # 'whitenoise.runserver_nostatic',
    # REST Framework
    "rest_framework",
    "rest_framework.authtoken",
    # "djoser",
    "djcelery_email",
    "phonenumber_field",
    "drf_recaptcha",
    'recurrence',
    # Django addons
    'anymail',
    "django_extensions",
    "django_filters",
    "embed_video",
    # 'channels',
    "ckeditor",
    "ckeditor_uploader",
    # APPS
    # "apps.auth",
    "apps.users",
    "apps.games",
    "apps.notifications",
    "rest_framework_tracking",
    "adminsortable2",
    "django_paranoid",
    "field_history"
    # "apps.sites.apps.SitesAppConfig",
]

PHONENUMBER_DB_FORMAT = 'E164'
# __  __________  ___  __   _____      _____   ___  ____
# /  |/  /  _/ _ \/ _ \/ /  / __/ | /| / / _ | / _ \/ __/
# / /|_/ // // // / // / /__/ _/ | |/ |/ / __ |/ , _/ _/
# /_/  /_/___/____/____/____/___/ |__/|__/_/ |_/_/|_/___/

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    # "backend.middleware.TimezoneMiddleware"
    # "apps.users.middleware.LocaleMiddleware",
]


###############
# DRF Recaptcha
DRF_RECAPTCHA_SECRET_KEY = "6LcMP_UUAAAAABVbPpiivQvMzw0i4d1bT6t-FWeO"
DRF_RECAPTCHA_DEFAULT_V3_SCORE = 0.2
DRF_RECAPTCHA_ACTION_V3_SCORES = {"register": 0.05}
DRF_RECAPTCHA_TESTING = DEBUG
#########
# ____________  ______  __   ___ ______________
# /_  __/ __/  |/  / _ \/ /  / _ /_  __/ __/ __/
# / / / _// /|_/ / ___/ /__/ __ |/ / / _/_\ \
# /_/ /___/_/  /_/_/  /____/_/ |_/_/ /___/___/

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BACKEND_DIR, "templates"), ],  # ["dist"],
        # "APP_DIRS": True, 
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                'django.template.loaders.app_directories.Loader',
                "admin_tools.template_loaders.Loader"
            ]
        },

    }
]

# ___  ______________
# / _ \/ __/ __/_  __/
# / , _/ _/_\ \  / /
# /_/|_/___/___/ /_/

DEFAULT_RENDERER_CLASSES = (
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated", ],
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',
        'user': '200/minute'
    }
}
if True:
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] += [
        "rest_framework.authentication.SessionAuthentication"
    ]

# ___     ______  ___________
# / _ \__ / / __ \/ __/ __/ _ \
# / // / // / /_/ /\ \/ _// , _/
# /____/\___/\____/___/___/_/|_|

DJOSER = {
    # "DOMAIN": ALLOWED_HOSTS[0],
    # 'SITE_NAME': 'net',
    "LOGIN_FIELD": "email",
    # 'USER_CREATE_PASSWORD_RETYPE':True,
    "ACTIVATION_URL": "activation/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "reset-pass/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "reset_email/{uid}/{token}",
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "USERNAME_RESET_SHOW_EMAIL_NOT_FOUND": True,
    # 'PASSWORD_RESET_CONFIRM_RETYPE': True,
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "SERIALIZERS": {
        "activation": "apps.users.serializers.ActivationSerializer",
        "user": "apps.users.serializers.UserSerializer",
        "user_create": "apps.users.serializers.UserCreateSerializer",
        "current_user": "apps.users.serializers.MyUserSerializer",
        # "password_reset": "apps.users.serializers.ReActivationSerializer",
    },
}

# ___  ___
# / _ \/ _ )
# / // / _  |
# /____/____/

DATABASES = {
    "default": {
        "CONN_MAX_AGE": 60,
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
        'DISABLE_SERVER_SIDE_CURSORS': True,
        # 'NAME': 'develop',
        # 'USER': 'guest',
        # 'PASSWORD': 'wlsad23_dop',
        # 'HOST': 'localhost',
        # 'PORT': 5432,
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
    }
}
#   ___  ___   ________  _   _____   __   _______  ___ ______________  _  __
#  / _ \/ _ | / __/ __/ | | / / _ | / /  /  _/ _ \/ _ /_  __/  _/ __ \/ |/ /
# / ___/ __ |_\ \_\ \   | |/ / __ |/ /___/ // // / __ |/ / _/ // /_/ /    /
# /_/  /_/ |_/___/___/   |___/_/ |_/____/___/____/_/ |_/_/ /___/\____/_/|_/

# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        )
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        'OPTIONS': {
            'min_length': 5,
        }
    },
    # {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    # {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# __   ____  ________   __   ____
# / /  / __ \/ ___/ _ | / /  / __/
# / /__/ /_/ / /__/ __ |/ /__/ _/
# /____/\____/\___/_/ |_/____/___/

# LANGUAGE_CODE = "en-us"  # 'en-us'
# TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
# LANGUAGES = [
#     ('ru', 'Russian'),
#     ('en', 'English'),
#     ]


# _____________ _______________
# / __/_  __/ _ /_  __/  _/ ___/
# _\ \  / / / __ |/ / _/ // /__
# /___/ /_/ /_/ |_/_/ /___/\___/

# When Vue Builds, path will be `/static/css/...` so we will have Django Serve
# In Production, it's recommended use an alternative approach such as:
# http://whitenoise.evans.io/en/stable/django.html?highlight=django

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# MIDDLEWARE_CLASSES = (
#     'whitenoise.middleware.WhiteNoiseMiddleware',
# )
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'django_yarnpkg.finders.NodeModulesFinder',
]

NODE_MODULES_ROOT = os.path.join(BACKEND_DIR, 'node_modules')

YARN_INSTALLED_APPS = (
    'chartjs-adapter-date-fns',
    'chart.js',
    'air-datepicker'
)

STATIC_URL = "/staticfiles/"
MEDIA_URL = "/media/"

################################################
EMBED_VIDEO_BACKENDS = (
    "embed_video.backends.YoutubeBackend",
    "embed_video.backends.VimeoBackend",
)

EMBED_VIDEO_TIMEOUT = 10

# __  __________  _______ _____   _  ____________
# /  |/  / __/ _ \/ ___/ // / _ | / |/ /_  __/ __/
# / /|_/ / _// , _/ /__/ _  / __ |/    / / / _\ \
# /_/  /_/___/_/|_|\___/_//_/_/ |_/_/|_/ /_/ /___/


LANGUAGE_CODE = 'ru'
# SITE_ID = int(os.getenv("SITE_ID", "0"))
MAIN_SITE_ID = int(os.getenv("MAIN_SITE_ID", "0"))
COMPANY_ID = int(os.getenv("COMPANY_ID", "0"))
# COMPANY_ID = 21
# logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {"format": "{levelname} {message}", "style": "{", },
        "tg": {
            "()": "python_telegram_logger.MarkdownFormatter",
            "fmt": " *%(levelname)s* _%(name)s : %(funcName)s_",
        },
    },
    "filters": {
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue", }, },
    "handlers": {
        "console": {
            "level": "DEBUG",
            # "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "console_force": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(SETTINGS_DIR, "django.log"),
            "maxBytes": 16777216,  # 16 MB
            "formatter": "verbose",
        },
        "file_error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(SETTINGS_DIR, "django_error.log"),
            "maxBytes": 16777216,  # 16 MB
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
        "telegram": {
            "level": "ERROR",
            "class": "python_telegram_logger.Handler",
            "token": "1198421957:AAG3j_ALcpCLhAcshA6z1xvnoVuIheyfMT8",
            "chat_ids": [88079841],
            "formatter": "tg",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file_error", "file"],
            "propagate": True,
            "level": "INFO",
        },
        "backend": {
            "handlers": ["console", "file_error", "file"],
            "level": "INFO",
        },
        "telegram_bot": {
            "handlers": ["console_force", "file_error", "file"],
            "level": "ERROR",
        },
        # todo separate logging
        "": {
            "handlers": ["console", "file_error", "file"],
            "level": "DEBUG",
        },
        # 'django.request': {
        # 'handlers': ['telegram','mail_admins'],
        # 'level': 'ERROR',
        # 'propagate': False,
        # },
        # 'gunicorn.errors': {
        #     'handlers': ['console'] if DEBUG else [] + ['file_error','file'],
        #     'level': 'INFO',
        # }
    },
}

####################################################

# ___________   _________  __
# / ___/ __/ /  / __/ _ \ \/ /
# / /__/ _// /__/ _// , _/\  /
# \___/___/____/___/_/|_| /_/

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'enterMode': 'CKEDITOR.ENTER_BR',
        'shiftEnterMode': 'CKEDITOR.ENTER_BR',
        'indent': False,
        'breakBeforeOpen': 'false',
        'breakAfterOpen': 'false',
        'breakBeforeClose': 'false',
        'breakAfterClose': 'false',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document',
             'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print',
                       '-', 'Templates']},
            {'name': 'clipboard',
             'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord',
                       '-', 'Undo', 'Redo']},
            {'name': 'editing',
             'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea',
                       'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
                       'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent',
                       'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight',
                       'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley',
                       'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles',
             'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

JAZZMIN_SETTINGS = {
    'site_title': 'Какие-то люди',
    'site_header': 'Какие-то люди',
    'site_brand': 'Какие-то люди',
    'site_logo': 'img/hashray_light.png',
    'welcome_sign': 'Какие-то люди: Админ панель',
    'hide_apps': ['graphql_auth', 'refresh_token'],
    'hide_models': ['auth.group', ],
    'changeform_format': 'collapsible',
    # font awesome v5
    'icons': {
        'farms.farm': 'fas fa-th-large',
        'farms.farmsgroup': 'fas fa-layer-group',
        'farms.farmacl': 'fas fa-user-lock',
        'miners.asicminer': 'fas fa-network-wired',
        'miners.asicfirmware': 'fas fa-microchip',
        'miners.asicfirmwareprofile': 'fas fa-ruler-vertical',
        'miners.poolgroup': 'fas fa-grip-horizontal',
        'miners.positiongroup': 'fas fa-grip-horizontal',
        'agents.agent': 'fas fa-server',
        'notifications.notification': 'fas fa-bell',
        'notifications.subscription': 'fas fa-link',
        'notifications.trigger': 'fas fa-exclamation',
        'errors.asicminererror': 'fas fa-exclamation-circle',
        'errors.agenterror': 'fas fa-exclamation-circle',
        'stats.asicminerstatistics': 'fas fa-chart-area',
        'stats.farmstatistics': 'fas fa-chart-area',
        'stats.poolgroupstatistics': 'fas fa-chart-area',
        'users.user': 'fas fa-users',
        'users.settings': 'fas fa-cog',
        'logs.ErrorLog': 'far fa-file-alt',
        'logs.TriggerLog': 'far fa-file-alt',
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": True,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": True,
    "brand_colour": "navbar-info",
    "accent": "accent-info",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-info",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}