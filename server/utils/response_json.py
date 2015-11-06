# coding=utf-8
from __future__ import absolute_import

from flask import current_app, request, make_response, json
from mongokit import Cursor
from errors.general_errors import ErrResponseInstanceTypeError
from errors.base_errors import APIError


class APIResponse(object):
    def __init__(self, status_code, internal_code, message=None):
        self.status_code = status_code
        self.response_code = internal_code
        self.status_message = message

    def __str__(self):
        return self.status_message


STATUS_OK = APIResponse(200, 0, "success")


def _content_data(rv):
    """The rv can be converted into a JSON-encoded data type"""
    if isinstance(rv, Cursor):
        return list(rv)
    return rv


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
    resp = make_response(json.dumps(output), response_or_error.status_code,
                         headers)
    return resp



def make_cors_headers():
    headers = dict()
    headers["Access-Control-Allow-Headers"] = make_allow_headers()
    headers[
        "Access-Control-Allow-Methods"] = "OPTIONS, HEAD, POST, PUT, DELETE"

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
    request_allows = request.headers.get("Access-Control-Request-Headers",
                                         None)
    if request_allows:
        return request_allows
    base_set = ["origin", "accept", "content-type", "authorization"]
    return ", ".join(base_set)