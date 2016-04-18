# coding=utf-8
from __future__ import absolute_import

import traceback
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, current_app, request
from mongokit import Connection as MongodbConn

from envs import CONFIG_NAME
from config import config
from utils.encoders import Encoder
from utils.api_utils import make_json_response, make_cors_headers
from apiresps.errors import (NotFound,
                             MethodNotAllowed,
                             UncaughtException)

from services.sup_oauth import SupOAuth


__version_info__ = ('0', '1', '5')
__version__ = '.'.join(__version_info__)

__artisan__ = ['Majik']


def create_app(config_name='development'):
    config_name = CONFIG_NAME or config_name

    app = Flask(__name__)

    app.version = __version__
    app.artisan = __artisan__

    # config
    app.config.from_object(config[config_name])
    app.json_encoder = Encoder
    app.debug = app.config.get("DEBUG")

    # logging
    if app.config.get("TESTING") is True:
        app.logger.setLevel(logging.FATAL)
    else:
        error_file_handler = RotatingFileHandler(
            app.config.get("LOGGING")["error"]["file"],
            maxBytes=app.config.get("LOGGING_ROTATING_MAX_BYTES"),
            backupCount=app.config.get("LOGGING_ROTATING_BACKUP_COUNT")
        )

        error_file_handler.setLevel(logging.WARNING)
        error_file_handler.setFormatter(
            logging.Formatter(app.config.get('LOGGING')['error']['format'])
        )

        app.logger.addHandler(error_file_handler)

    # database connections
    app.mongodb_database = MongodbConn(
        host=app.config.get("DB_HOST"),
        port=app.config.get("DB_PORT"))
    app.mongodb_conn = app.mongodb_database[
        app.config.get("DB_DBNAME")]

    app.sup_oauth = SupOAuth(
        ext_key=app.config.get("EXT_KEY"),
        ext_secret=app.config.get("EXT_SECRET"),
        secret_key=app.config.get("SECRET_KEY"),
        expires_in=app.config.get("EXPIRES_IN"),
        api_uri=app.config.get("OAUTH_API_URI"),
        token_uri=app.config.get("OAUTH_TOKEN_API_URI"),
        redirect_uri=app.config.get("OAUTH_REDIRECT_URI")
    )

    from blueprints.user.models import ExtUser
    app.mongodb_database.register([ExtUser])

    # register blueprints
    from blueprints.user import blueprint as user_module
    app.register_blueprint(user_module, url_prefix="/user")

    from blueprints.comment import blueprint as comment_module
    app.register_blueprint(comment_module, url_prefix="/comment")

    # register error handlers
    @app.errorhandler(404)
    def app_error_404(error):
        current_app.logger.warn(
            "Error: 404\n{}".format(traceback.format_exc()))
        return make_json_response(NotFound())

    @app.errorhandler(405)
    def app_error_405(error):
        current_app.logger.warn(
            "Error: 405\n{}".format(traceback.format_exc()))
        return make_json_response(MethodNotAllowed())

    @app.errorhandler(Exception)
    def app_error_uncaught(error):
        current_app.logger.warn(
            "Error: Uncaught\n{}".format(traceback.format_exc()))
        return make_json_response(UncaughtException(repr(error)))

    @app.before_request
    def app_before_request():
        # cors response
        if request.method == "OPTIONS":
            resp = current_app.make_default_options_response()
            cors_headers = make_cors_headers()
            resp.headers.extend(cors_headers)
            return resp

    print "-------------------------------------------------------"
    print "Comment Extension: {}".format(app.version)
    print "Developers: {}".format(', '.join(app.artisan))
    print "-------------------------------------------------------"

    return app
