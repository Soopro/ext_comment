# coding=utf-8
from __future__ import absolute_import

from .base_errors import APIError
import httplib


class MemberPasswordNotMatch(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 14001
    status_message = "PASSWORD_NOT_MATCH"


class MemberInvalidProfile(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 14002
    status_message = "INVALID_MEMBER_PROFILE"


class MemberDuplicateLogin(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 14003
    status_message = "DUPLICATE_LOGIN"


class MemberNotFound(APIError):
    status_code = httplib.NOT_FOUND
    response_code = 14004
    status_message = "MEMBER_NOT_FOUND"


class MemberWrongPassword(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 14005
    status_message = "WRONG_PASSWORD"


class RoleNotFound(APIError):
    status_code = httplib.NOT_FOUND
    response_code = 14006
    status_message = "ROLE_NOT_FOUND"


class RoleNotOwner(APIError):
    status_code = httplib.FORBIDDEN
    response_code = 14007
    status_message = "ROLE_NOT_OWNER"


class RoleDuplicate(APIError):
    status_code = httplib.FORBIDDEN
    response_code = 14008
    status_message = "ROLE_ALREADY_EXIST"

class RoleReachedLimit(APIError):
    status_code = httplib.FORBIDDEN
    response_code = 14009
    status_message = "ROLE_REACHED_LIMIT"
    
class MemberRelateDuplicate(APIError):
    status_code = httplib.FORBIDDEN
    response_code = 14100
    status_message = "MEMBER_ALREADY_RELATED"


class OwnerNotFound(APIError):
    status_code = httplib.NOT_FOUND
    response_code = 14110
    status_message = "OWNER_NOT_FOUND"


class OwnerAlreadyExist(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 14111
    status_message = "OWNER_ALREADY_EXIST"


class ActivityNotFound(APIError):
    status_code = httplib.NOT_FOUND
    response_code = 14121
    status_message = "ACTIVITY_NOT_FOUND"


class ActivityDuplicate(APIError):
    status_code = httplib.FORBIDDEN
    response_code = 14122
    status_message = "ACTIVITY_ALREADY_EXIST"


class ActivityReachedLimit(APIError):
    status_code = httplib.FORBIDDEN
    response_code = 14123
    status_message = "ACTIVITY_REACHED_LIMIT"


class ApplymentNotFound(APIError):
    status_code = httplib.NOT_FOUND
    response_code = 14131
    status_message = "APPLYMENT_NOT_FOUND"