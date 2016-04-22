# coding=utf-8
from __future__ import absolute_import

import os
from datetime import timedelta


class Config(object):
    DEBUG = True
    SECRET_KEY = 'comment_999'

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    DB_HOST = '127.0.0.1'
    DB_PORT = 27017

    ALLOW_ORIGINS = ['*']
    ALLOW_CREDENTIALS = False

    EXT_KEY = 'comment-custom'
    EXT_SECRET = 'comment-custom-2016'

    EXPIRES_IN = timedelta(seconds=3600 * 24 * 30)

    OAUTH_API_URI = 'http://api.soopro.com'
    OAUTH_TOKEN_API_URI = '{}/oauth/token'.format(OAUTH_API_URI)
    OAUTH_REDIRECT_URI = 'http://sup.local:8888/#/auth/redirect'

    CURL_BASE_URL = 'http://localhost:5001/comment'

    MEMBER_URL = "{}/crm/member".format(OAUTH_API_URI)

    # logging
    LOG_FOLDER = os.path.join(BASE_DIR, 'deploy')
    LOGGING = {
        'error': {
            'format': '%(asctime)s %(levelname)s: %(message)s' +
                      ' [in %(pathname)s:%(lineno)d]',
            'file': os.path.join(LOG_FOLDER, "error.log")
        }
    }

    LOGGING_ROTATING_MAX_BYTES = 64 * 1024 * 1024
    LOGGING_ROTATING_BACKUP_COUNT = 5


class DevelopmentConfig(Config):
    DB_DBNAME = 'ext_comment_dev'


class TestCaseConfig(Config):
    DB_DBNAME = 'ext_comment_testcase'


class TestingConfig(Config):
    DEBUG = False
    DB_DBNAME = 'ext_comment_test'

    EXT_KEY = 'comment-1460987711'
    EXT_SECRET = '477a39f0-ff8f-4af6-b596-ce9d9d914f94'

    OAUTH_API_URI = 'http://api.sup.farm'
    OAUTH_TOKEN_API_URI = '{}/oauth/token'.format(OAUTH_API_URI)
    OAUTH_REDIRECT_URI = 'http://comm.exts.sup.farm/#/auth/redirect'

    CURL_BASE_URL = 'http://api-comm.exts.sup.farm/commment'


class ProductionConfig(Config):
    DEBUG = False
    DB_DBNAME = 'ext_comment_prd'

    EXT_KEY = 'comment-1460987711'
    EXT_SECRET = '477a39f0-ff8f-4af6-b596-ce9d9d914f94'

    OAUTH_API_URI = 'http://api.soopro.com'
    OAUTH_TOKEN_API_URI = '{}/oauth/token'.format(OAUTH_API_URI)
    OAUTH_REDIRECT_URI = 'http://comm.exts.soopro.net/#/auth/redirect'

    CURL_BASE_URL = 'http://api-comm.exts.soopro.net/commment'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    "testcase": TestCaseConfig,
    'default': DevelopmentConfig
}
