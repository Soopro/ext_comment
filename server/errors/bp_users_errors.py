#coding=utf-8
from __future__ import absolute_import
import httplib

from .base_errors import APIError


class SooproRequestAccessTokenError(APIError):
    status_code = httplib.INTERNAL_SERVER_ERROR
    status_message = "Soopro Request Access Token Error"
    response_code = 10001


class SooproAccessDeniedError(APIError):
    status_code = httplib.INTERNAL_SERVER_ERROR
    status_message = "Soopro Access Denied Error"
    response_code = 10002


class SooproAPIError(APIError):
    status_code = httplib.INTERNAL_SERVER_ERROR
    status_message = "Soopro API requests Error"
    response_code = 10003

