# coding=utf-8
from __future__ import absolute_import

from datetime import timedelta

__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)


class Config(object):
    version = __version__
    DEBUG = True

    HOST = "127.0.0.1"
    PORT = 5001

    EXT_COMMENT_DB_HOST = '127.0.0.1'
    EXT_COMMENT_DB_PORT = 27017

    SECRET_KEY = 'secret_key'

    ALLOW_ORIGINS = ['*']
    ALLOW_CREDENTIALS = False

    APP_KEY = 'url4-1443411015'
    APP_SECRET = 'feff7961-c2df-410d-b581-711adff34c16'
    GRANT_TYPE = 'code'

    REMOTE_OAUTH_URL = 'http://d.sup.farm/#/oauth'
    TOKEN_URL = 'http://api.sup.farm/oauth/token'

    REDIRECT_URI = 'http://localhost:9527/#/redirect'
    EXPIRED_IN = 36000

    # JWT
    JWT_SECRET_KEY = SECRET_KEY  # SECRET_KEY
    JWT_ALGORITHM = 'HS256'
    JWT_VERIFY_EXPIRATION = True,
    JWT_LEEWAY = 0
    JWT_EXPIRATION_DELTA = timedelta(seconds=3600 * 24 * 30)
    JWT_DEFAULT_REALM = 'Login Required'


class DevelopmentConfig(Config):
    EXT_COMMENT_DB_DBNAME = 'ext_comment_dev'


class TestCaseConfig(Config):
    EXT_COMMENT_DB_DBNAME = 'ext_comment_testcase'


class TestingConfig(Config):
    EXT_COMMENT_DB_DBNAME = 'ext_comment_test'


class ProductionConfig(Config):
    DEBUG = False
    EXT_COMMENT_DB_DBNAME = 'ext_comment_production'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    "testcase": TestCaseConfig,
    'default': DevelopmentConfig
}
