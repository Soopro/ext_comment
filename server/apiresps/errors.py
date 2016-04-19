# coding=utf-8
from __future__ import absolute_import
import httplib

from .base import APIError


# not found
class NotFound(APIError):
    status_code = httplib.NOT_FOUND
    status_message = 'RESOURCE_NOT_FOUND'
    response_code = 100000


# forbidden
class PermissionDenied(APIError):
    status_code = httplib.FORBIDDEN
    status_message = 'FORBIDDEN'
    response_code = 101000


class PermissionExpired(PermissionDenied):
    status_message = 'EXPIRED'
    response_code = 101001


# unauthorized
class AuthFailed(APIError):
    status_code = httplib.UNAUTHORIZED
    status_message = 'AUTHENTICATION_FAILED'
    response_code = 102000


# not allow
class MethodNotAllowed(APIError):
    status_code = httplib.METHOD_NOT_ALLOWED
    status_message = 'REQUEST_METHOD_NOT_ALLOWED'
    response_code = 103000


class RequestMaxLimited(MethodNotAllowed):
    response_code = 103001
    status_message = "REQUEST_REACHES_MAX_LIMIT"


class RequestBlocked(MethodNotAllowed):
    response_code = 103002
    status_message = "REQUEST_BLOCKED"


# bad request
class BadRequest(APIError):
    status_code = httplib.BAD_REQUEST
    status_message = 'BAD_REQUEST'
    response_code = 104000


class RequestSourceNotExists(BadRequest):
    response_code = 104001
    status_message = "REQUEST_SOURCE_NOT_EXISTS"


class InvalidRequest(BadRequest):
    response_code = 104002
    status_message = "INVALID_REQUEST"


# internal server error
class InternalServerError(APIError):
    status_code = httplib.INTERNAL_SERVER_ERROR
    response_code = 105000
    status_message = "INTERNAL_SERVER_ERROR"


class ResponseInstanceTypeError(InternalServerError):
    response_code = 105001
    status_message = "API_RESPONSE_TYPE_ERROR"


class UncaughtException(InternalServerError):
    response_code = 105002
    status_message = "UNCAUGHT_EXCEPTION"


class MongoDBError(InternalServerError):
    response_code = 105003
    status_message = "MONGODB_ERROR"


# conflict
class ConflictError(APIError):
    status_code = httplib.CONFLICT
    status_message = 'CONFLICT_ERROR'
    response_code = 106000


# unexpection
class Unexpected(APIError):
    status_code = httplib.EXPECTATION_FAILED
    status_message = 'UNEXPECTED'
    response_code = 107000


class ValidationError(Unexpected):
    response_code = 107001
    status_message = 'INVALID_DATA'


# app
class AppNotFoundOrNotOwner(NotFound):
    response_code = 108001
    status_message = "APP_NOT_FOUND"


class AppTrunkNotFound(NotFound):
    response_code = 108002
    status_message = "APP_TRUNK_NOT_FOUND"


# user
class UserNotFound(NotFound):
    response_code = 109001
    status_message = 'USER_NOT_FOUND'


# customer
class CustomerNotFound(NotFound):
    response_code = 110001
    status_message = 'CUSTOMER_NOT_FOUND'


class CustomerAlreadyExist(ConflictError):
    response_code = 110002
    status_message = 'CUSTOMER_ALREADY_EXIST'


class CreateCustomerFailed(Unexpected):
    response_code = 110003
    status_message = 'CREATE_CUSTOMER_FAILED'


# file
class FileCreateFailed(Unexpected):
    status_message = 'MAKE_FILE_FAILED'
    response_code = 111001


class FileDeleteFailed(Unexpected):
    status_message = 'DELETE_FILE_FAILED'
    response_code = 111002


class FileNotFound(Unexpected):
    status_message = 'FILE_NOT_FOUND'
    response_code = 111003


class FileExist(ConflictError):
    status_message = 'FILE_PATH_EXIST'
    response_code = 111004


class FileNameInvalid(ValidationError):
    response_code = 111005
    status_message = 'EMPTY_NAME_INVALID'


# theme
class ThemeNotFound(NotFound):
    status_code = httplib.NOT_FOUND
    response_code = 112001
    status_message = "THEME_NOT_FOUND"


class ThemeInvalidUploadFile(BadRequest):
    response_code = 112002
    status_message = "THEME_UPLOAD_FILE_FAILED"


class ThemeUploadBadZipFile(BadRequest):
    response_code = 112003
    status_message = "THEME_INVALID_ZIP_FILE"


class ThemeCustomFolderNotExist(NotFound):
    response_code = 112004
    status_message = "CUSTOM_THEME_NOT_FOUND"


class ThemeCustomRemoveFailed(InternalServerError):
    response_code = 112005
    status_message = "CUSTOM_THEME_REMOVE_FAILED"


class ThemeConfigInvalid(InternalServerError):
    response_code = 112006
    status_message = "THEME_CONFIG_INVALID"


class ThemeTemplateFileNotFound(NotFound):
    response_code = 112007
    status_message = "TEMPLATE_FILE_NOT_FOUND"


class ThemeTemplateFileInvalid(ValidationError):
    response_code = 112008
    status_message = "TEMPLATE_FILE_INVALID"


class ThemeTemplateFileCircularInclude(InternalServerError):
    response_code = 112009
    status_message = "TEMPLATE_FILE_CIRCULAR_INCLUDE"


class ThemeTemplateFileSizeTooLarge(Unexpected):
    response_code = 112010
    status_message = "TEMPLATE_FILE_SIZE_TOO_LARGE"


class ThemeTemplateOverload(Unexpected):
    response_code = 112011
    status_message = "TEMPLATE_OVERLOAD"


class ThemePresetsInvalid(InternalServerError):
    response_code = 112012
    status_message = "THEME_PRESETS_INVALID"


class ThemeContextInvalid(InternalServerError):
    response_code = 112013
    status_message = "THEME_CONTEXT_INVALID"


class ThemeTranslatesInvalid(InternalServerError):
    response_code = 112014
    status_message = "THEME_TRANSLATES_INVALID"


# extension
class ExtensionNotFound(NotFound):
    response_code = 113001
    status_message = "EXTENSION_NOT_FOUND"


class ExtensionMaxLimited(BadRequest):
    response_code = 113002
    status_message = "EXTENSION_NUM_REACHES_MAX_LIMIT"


class ExtensionAlreadyActivated(ConflictError):
    response_code = 113003
    status_message = "EXTENSION_ALREADY_ACTIVATED"


class ExtensionNotActivated(BadRequest):
    response_code = 113004
    status_message = "EXTENSION_NOT_ACTIVATED"


class ExtensionInvalidUploadFileFailed(BadRequest):
    response_code = 113005
    status_message = "EXTENSION_UPLOAD_FILE_FAILED"


class ExtensionConfigInvalid(InternalServerError):
    response_code = 113006
    status_message = "EXTENSION_CONFIG_INVALID"


class ExtensionNotPurchased(NotFound):
    response_code = 113007
    status_message = "EXTENSION_NOT_PURCHASED"


class ExtensionNotInstallable(InternalServerError):
    response_code = 113008
    status_message = "EXTENSION_NOT_INSTALLABLE"


class ExtensionInvalidSlots(InternalServerError):
    response_code = 113009
    status_message = "EXTENSION_BAD_SLOTS"


# content
class ContentNotFound(NotFound):
    response_code = 114001
    status_message = "CONTENT_NOT_FOUND"


class ContentExists(ConflictError):
    response_code = 114002
    status_message = "CONTENT_EXISTS"


class ContentFileNotAllowed(MethodNotAllowed):
    response_code = 114003
    status_message = "CONTENT_NOT_ALLOWED"


class ContentTypeNotFound(NotFound):
    response_code = 114004
    status_message = "CONTENT_TYPE_NOT_FOUND"


class ContentTypeExists(ConflictError):
    response_code = 114005
    status_message = "CONTENT_TYPE_EXISTS"


class ContentTypeNotAllowed(MethodNotAllowed):
    response_code = 114006
    status_message = "CONTENT_TYPE_NOT_ALLOWED"


class ContentNotEnoughStorage(MethodNotAllowed):
    response_code = 114007
    status_message = "CONTENT_NOT_ENOUGH_STORAGE"


class ContentNotEnoughLiveStorage(MethodNotAllowed):
    response_code = 114008
    status_message = "CONTENT_NOT_ENOUGH_LIVE_STORAGE"


# taxonomy
class TaxonomyNotFound(NotFound):
    response_code = 115001
    status_message = "TEXONOMY_NOT_FOUND"


class TaxonomyExists(ConflictError):
    response_code = 115002
    status_message = "TEXONOMY_ALIAS_EXISTS"


class TermBadParents(BadRequest):
    response_code = 115003
    status_message = "TERM_BAD_PARENTS"


class TermNotFound(NotFound):
    response_code = 115004
    status_message = "TERM_NOT_FOUND"


class TermExists(ConflictError):
    response_code = 115005
    status_message = "TERM_ALIAS_EXISTS"


# menu
class MenuNotFound(NotFound):
    response_code = 116001
    status_message = "MENU_NOT_FOUND"


class MenuExists(ConflictError):
    response_code = 116002
    status_message = "MENU_ALIAS_EXISTS"
