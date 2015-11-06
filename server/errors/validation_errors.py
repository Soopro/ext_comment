# coding=utf-8
from __future__ import absolute_import

import httplib
import re
from bson import ObjectId
from bson.errors import InvalidId
from .base_errors import APIError


class ValidationParameterRequired(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 98001
    status_message = "PARAMETER_REQUIRED"

    def __init__(self, name=""):
        super(ValidationParameterRequired, self).__init__(name)
        return


class ValidationParameterBlank(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 98002
    status_message = "PARAMETER_MUST_NOT_BE_BLANK"

    def __init__(self, name=""):
        super(ValidationParameterBlank, self).__init__(name)
        return


class ValidationParameterMaxLimit(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 98003
    status_message = "PARAMETER_REACHES_THE_MAX_LENGTH"

    def __init__(self, name=""):
        super(ValidationParameterMaxLimit, self).__init__(name)
        return


class ValidationParameterMinLimit(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 98004
    status_message = "PARAMETER_REACHES_THE_MIN_LENGTH"

    def __init__(self, name=""):
        super(ValidationParameterMinLimit, self).__init__(name)
        return


class ValidationParameterInvalidEmail(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 98005
    status_message = "INVALID_EMAIL_ADDRESS"

    def __init__(self, name=""):
        super(ValidationParameterInvalidEmail, self).__init__(name)
        return


class ValidationParameterInvalidAlias(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 98006
    status_message = "INVALID_ALIAS"

    def __init__(self, name=""):
        super(ValidationParameterInvalidAlias, self).__init__(name)
        return


class ValidationParameterInvalidObjectType(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 98007
    status_message = "INVALID_OBJECT_TYPE"

    def __init__(self, name=""):
        super(ValidationParameterInvalidObjectType, self).__init__(name)
        return


class ValidationParameterInvalidObjectId(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 98008
    status_message = "INVALID_OBJECT_ID"

    def __init__(self, name=""):
        super(ValidationParameterInvalidObjectId, self).__init__(name)
        return


class ValidationParameterValueMin(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 98009
    status_message = "PARAMETER_VALUE_TOO_SMALL"

    def __init__(self, name=""):
        super(ValidationParameterValueMin, self).__init__(name)
        return


class ValidationParameterValueMax(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 98010
    status_message = "PARAMETER_VALUE_TOO_LARGE"

    def __init__(self, name=""):
        super(ValidationParameterValueMax, self).__init__(name)
        return


class ValidationParameterInvalid(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 98011
    status_message = "PARAMETER_INVALID"

    def __init__(self, name=""):
        super(ValidationParameterInvalid, self).__init__(name)
        return


class ParamStructure(object):
    name = None
    type = None
    format_ObjectId = False
    format_alias = False
    non_empty = False
    len_min = None
    len_max = None
    value_min = None
    value_max = None

    def __init__(self, value, name=None, non_empty=None):
        self.value = value
        if name is not None:
            self.name = name
        if non_empty is not None:
            self.non_empty = bool(non_empty)
        self._validate()
        return

    def _validate(self):
        if self.non_empty is True:
            self._validate_non_empty()
        elif self.value is None:
            return

        if self.type is not None:
            self._validate_type()

        if self.format_ObjectId:
            self._validate_object_id()
        elif self.format_alias:
            self._validate_alias()

        self.value = self.pre_handler()

        if self.len_min is not None:
            self._validate_len_min()

        if self.len_max is not None:
            self._validate_len_max()

        if self.value_min is not None:
            self._validate_value_min()

        if self.value_max is not None:
            self._validate_value_max()

        if self.validator() is False:
            raise ValidationParameterInvalid(self.name)
        return

    def _validate_type(self):
        if not isinstance(self.value, self.type):
            raise ValidationParameterInvalidObjectType(self.name)

    def _validate_object_id(self):
        try:
            ObjectId(self.value)
        except InvalidId:
            raise ValidationParameterInvalidObjectId(self.name)

    def _validate_alias(self):
        alias_pattern = re.compile(r'[\w-]+$')
        if not self.value or not alias_pattern.match(self.value):
            ValidationParameterInvalidAlias(self.name)

    def _validate_non_empty(self):
        if not bool(
                self.value) and self.value is not 0 and self.value is not False:
            raise ValidationParameterBlank(self.name)

    def _validate_len_min(self):
        if len(self.value) < self.len_min:
            raise ValidationParameterMinLimit(self.name)

    def _validate_len_max(self):
        if len(self.value) > self.len_max:
            raise ValidationParameterMaxLimit(self.name)

    def _validate_value_min(self):
        if self.value < self.value_min:
            raise ValidationParameterValueMin(self.name)

    def _validate_value_max(self):
        if self.value > self.value_max:
            raise ValidationParameterValueMax(self.name)

    def validator(self):
        pass

    def pre_handler(self):
        return self.value


# Parameter structure preset
class ObjectIdStructure(ParamStructure):
    non_empty = True
    format_ObjectId = True


# class AliasStructure(ParamStructure):
#     len_max = 100
#     non_empty = True
#     format_alias = True
#     type = unicode
#
#
# class SIDStructure(ParamStructure):
#     non_empty = True
#     len_max = 146
#     type = unicode


class DictStructure(ParamStructure):
    non_empty = True
    type = dict


class AttrStructure(ParamStructure):
    len_max = 100
    non_empty = True
    type = unicode


# class DescStructure(ParamStructure):
#     len_max = 500
#     non_empty = True
#     type = unicode


class TokenStructure(ParamStructure):
    len_max = 500
    non_empty = True
    type = unicode


class ContentStructure(ParamStructure):
    non_empty = True
    type = unicode


class ListStructure(ParamStructure):
    non_empty = True
    type = list


# class FileStructure(ParamStructure):
#     non_empty = True
#     type = None


class OrderStructure(ParamStructure):
    non_empty = True
    type = int


class StatusStructure(ParamStructure):
    non_empty = True
    type = int


# class LengthStructure(ParamStructure):
#     non_empty = True
#     type = int
#
#
# class IntegerStructure(ParamStructure):
#     non_empty = True
#     type = int
#
#
# class BoolStructure(ParamStructure):
#     non_empty = True
#     type = bool


class UrlStructure(ParamStructure):
    len_max = 500
    non_empty = True
    type = unicode


# class ProtocolStructure(ParamStructure):
#     len_max = 10
#     non_empty = True
#     type = unicode
#
#
# class DomainStructure(ParamStructure):
#     len_max = 100
#     non_empty = True
#     type = unicode
#
#
# class EmailStructure(ParamStructure):
#     len_max = 150
#     non_empty = True
#     type = unicode
#
#
# class FlagBitStructure(ParamStructure):
#     non_empty = True
#     value_min = 0
#     value_max = 100
#     type = int
#
#
# class LoginStructure(ParamStructure):
#     non_empty = True
#     len_max = 200
#     type = unicode
#
#
# class PasswordStructure(ParamStructure):
#     non_empty = True
#     len_max = 50
#     type = unicode
