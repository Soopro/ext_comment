# -*- coding: utf-8 -*-

__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)

class Config(object):
    version = __version__
    DEBUG = True

    HOST = "127.0.0.1"
    PORT = 5001

    EXT_COMMENT_DB_HOST = '127.0.0.1'
    EXT_COMMENT_DB_PORT = 27017

    REDIRECT_URL_DOMAIN = 'http://url4.cc'

    SECRET_KEY = 'secret_key'

    ALLOW_ORIGINS = ['*']
    ALLOW_CREDENTIALS = False

    AUTH_URL = 'http://127.0.0.1:9002/#/oauth2'
    TOKEN_URL = 'http://127.0.0.1:5000/auth2/token'

    APP_KEY = 'url4cc-1431520320'
    APP_SECRET = 'feff7961-c2df-410d-b581-711adff34c16'
    GRANT_TYPE = 'code'

    REDIRECT_URI = 'http://127.0.0.1:9000/#/redirect'
    EXPIRED_IN = 36000


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
