# coding=utf-8
from __future__ import absolute_import

from flask import current_app, request, make_response, json
from functools import wraps
from mongokit import Cursor

from apiresps import APIResponse, APIError, STATUS_OK
from apiresps.errors import ResponseInstanceTypeError


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


def _make_allow_headers():
    request_allows = request.headers.get("Access-Control-Request-Headers",
                                         None)
    if request_allows:
        return request_allows
    base_set = ["origin", "accept", "content-type", "authorization"]
    return ", ".join(base_set)


def make_cors_headers():
    headers = dict()
    headers["Access-Control-Allow-Headers"] = _make_allow_headers()
    headers_options = "OPTIONS, HEAD, POST, PUT, DELETE"
    headers["Access-Control-Allow-Methods"] = headers_options

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


def make_json_response(response_or_error=STATUS_OK, data=None, cross=True):
    if isinstance(response_or_error, APIResponse):
        output = data
    else:
        if not isinstance(response_or_error, APIError):
            response_or_error = ResponseInstanceTypeError()

        if request.method in ['PUT', 'POST']:
            try:
                request_body = request.json
            except Exception:
                request_body = u'Json Data Invalid'
        else:
            request_body = u''

        output = {
            "errcode": response_or_error.response_code,
            "errmsg": response_or_error.status_message,
            "erraffix": response_or_error.affix_message,
            "request": {
                "request_api": request.path,
                "request_method": request.method,
                "request_body": request_body,
            }
        }
    headers = dict()
    headers["Content-Type"] = "application/json"
    if cross is True:
        headers.update(make_cors_headers())

    resp = make_response(json.dumps(output),
                         response_or_error.status_code,
                         headers)
    return resp
