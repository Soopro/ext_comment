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

    EXT_KEY = 'comment-1451985732'
    EXT_SECRET = '7c3b8024-6985-41e3-8c92-aeb687481ee1'
    GRANT_TYPE = 'code'

    REMOTE_OAUTH_URL = 'http://d.soopro.com/#/oauth'
    TOKEN_URL = 'http://api.soopro.com/oauth/token'

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
    TOKEN_URL = 'http://127.0.0.1:5000/oauth/token'
    REMOTE_OAUTH_URL = 'http://sup.local:9526/#/oauth'
    
    EXT_KEY = 'comment-1452073523'
    EXT_SECRET = '95552db4-f9d7-4158-ada2-e248cce42ea3'

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
