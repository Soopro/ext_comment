# coding=utf-8
from __future__ import absolute_import

from apiresps.errors import (AuthFailed,
                             InternalServerError,
                             PermissionDenied,
                             NotFound)


class RequestAccessTokenFailed(PermissionDenied):
    status_message = "REQUEST_ACCESS_TOKEN_FAILED"
    response_code = 300001


class RefreshAccessTokenFailed(PermissionDenied):
    status_message = "REFRESH_ACCESS_TOKEN_FAILED"
    response_code = 300002


class LogoutAccessTokenFailed(InternalServerError):
    status_message = "LOGOUT_ACCESS_TOKEN_FAILED"
    response_code = 300003


class AccessDenied(InternalServerError):
    status_message = "ACCESS_DENIED"
    response_code = 300004


class RemoteAPIFailed(InternalServerError):
    status_message = "REQUEST_REMOTE_API_FAILED"
    response_code = 300005


class UserTokenFailed(NotFound):
    status_message = "USER_TOKEN_FAILED"
    response_code = 300006


class UserNotFound(NotFound):
    status_message = "USER_NOT_FOUND"
    response_code = 300007


class UserStateInvalid(PermissionDenied):
    status_message = "USER_STATE_INVALID"
    response_code = 300008


class UserProfileFailed(InternalServerError):
    status_message = "USER_PROFILE_FAILED"
    response_code = 300009
