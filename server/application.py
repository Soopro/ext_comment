# coding=utf-8
from __future__ import absolute_import

import traceback
from flask import Flask, current_app
from mongokit import Connection as MongodbConn
from config import config
from utils.encoders import Encoder
from utils.ext_oauth import SupAuth
from utils.base_utils import make_json_response
from errors.general_errors import (NotFound, ErrUncaughtException,
                                   MethodNotAllowed)


def create_app(config_name='development'):
    app = Flask(__name__)
    # config
    app.config.from_object(config[config_name])
    app.json_encoder = Encoder

    # database connections
    app.mongodb_database = MongodbConn(
        host=app.config.get("EXT_COMMENT_DB_HOST"),
        port=app.config.get("EXT_COMMENT_DB_PORT"))
    app.mongodb_conn = app.mongodb_database[
        app.config.get("EXT_COMMENT_DB_DBNAME")]

    app.sup_auth = SupAuth(app_key=app.config.get("APP_KEY"),
                           app_secret=app.config.get("APP_SECRET"),
                           grant_type=app.config.get("GRANT_TYPE"),
                           secret_key=app.config.get("SECRET_KEY"),
                           redirect_uri=app.config.get("REDIRECT_URI"),
                           expired_in=app.config.get("EXPIRED_IN"))

    # inject database connections to app object
    # app.mongodb_database = mongodb_database
    # app.mongodb_conn = mongodb_conn

    # register mongokit models
    from blueprints.extension.models import (CommentExtension,
                                             CommentGroup, Comment)

    app.mongodb_database.register([CommentExtension, CommentGroup, Comment])

    # register blueprints
    from blueprints.extension import blueprint as comment_blueprint
    app.register_blueprint(comment_blueprint)

    from blueprints.user import blueprint as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/comment/user")

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
    def app_error_500(error):
        current_app.logger.warn(
            "Error: 500\n{}".format(traceback.format_exc()))
        return make_json_response(ErrUncaughtException(repr(error)))

    return app
