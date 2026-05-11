# -*- coding: utf-8 -*-

from .settings import *     # noqa


# 環境の種類。独自の変数。
ENVIRONMENT = 'test'

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
EMAIL_PORT = 1025

STATIC_ROOT = None


# これを設定しないとテストできない。
DEBUG_TOOLBAR_CONFIG = {
    'IS_RUNNING_TESTS': False
}
