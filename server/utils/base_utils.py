# coding=utf-8
from __future__ import absolute_import

from functools import wraps

from flask import make_response, json, current_app, request
from mongokit.cursor import Cursor
from errors.base_errors import APIError
import httplib
import time


def generate_current_second():
    return unicode(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))


def generate_time():
    millsecond = time.time()
    return millsecond


def now():
    return int(time.time()*1000)


class APIResponse(object):
    def __init__(self, status_code, internal_code, message=None):
        self.status_code = status_code
        self.response_code = internal_code
        self.status_message = message

    def __str__(self):
        return self.status_message


STATUS_OK = APIResponse(200, 0, "success")


class ErrResponseInstanceTypeError(APIError):
    status_code = httplib.INTERNAL_SERVER_ERROR
    response_code = 10000
    response_message = "API_TYPE_ERROR: Not APIError"


def _content_data(rv):
    """The rv can be converted into a JSON-encoded data type"""
    if isinstance(rv, Cursor):
        return list(rv)
    return rv


def output_json(f):
    @wraps(f)
    def decorate(*args, **kwargs):
        result = f(*args, **kwargs)
        data = _content_data(result)
        return make_json_response(STATUS_OK, data)
    return decorate


def make_json_response(response_or_error, data=None, cross=True):
    if isinstance(response_or_error, APIResponse):
        output = data
    else:
        if not isinstance(response_or_error, APIError):
            response_or_error = ErrResponseInstanceTypeError()
        try:
            json_data = request.json
        except Exception:
            json_data = "Json Data Invalid"

        output = {
            "errcode": response_or_error.response_code,
            "errmsg": response_or_error.status_message,
            "erraffix": response_or_error.affix_message,
            "request": {
                "request_api": request.path,
                "request_method": request.method,
                "request_body": json_data,
            }
        }
    headers = dict()
    headers["Content-Type"] = "application/json"
    if cross is True:
        headers.update(make_cors_headers())
    resp = make_response(json.dumps(output), response_or_error.status_code, headers)
    return resp


def make_cors_headers():
    headers = dict()
    headers["Access-Control-Allow-Headers"] = make_allow_headers()
    headers["Access-Control-Allow-Methods"] = "OPTIONS, HEAD, POST, PUT, DELETE"

    allowed_origins = current_app.config.get('ALLOW_ORIGINS', [])
    allowed_credentials = current_app.config.get('ALLOW_CREDENTIALS')

    if '*' in allowed_origins:
        headers["Access-Control-Allow-Origin"] = '*'
    elif request.headers.get('Origin') in allowed_origins:
        headers["Access-Control-Allow-Origin"] = request.headers['Origin']

    if allowed_credentials:
        headers["Access-Control-Allow-Credentials"] = 'true'

    headers["Access-Control-Max-Age"] = 60 * 60 * 24
    return headers


def make_allow_headers():
    request_allows = request.headers.get("Access-Control-Request-Headers", None)
    if request_allows:
        return request_allows
    base_set = ["origin", "accept", "content-type", "authorization"]
    return ", ".join(base_set)


class Url(object):
    def __init__(self, path, func, method, **options):
        if isinstance(method, str):
            method = method.split(' ')
        self.path = path
        self.methods = method
        self.func = func
        self.options = options


def url(path, f, method='GET', **options):
    return Url(path, f, method, **options)


def route_inject(app_or_blueprint, url_patterns):
    for pattern in url_patterns:
        if isinstance(pattern, tuple):
            path, func, method = pattern
            pattern = url(path, func, method)
        app_or_blueprint.route(pattern.path, methods=pattern.methods, **pattern.options)(pattern.func)