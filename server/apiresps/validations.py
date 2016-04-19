#coding=utf-8
from __future__ import absolute_import

from bson import ObjectId
import re

from .base import APIError
from .errors import BadRequest, ValidationError


class ValidationParameterRequired(ValidationError):
    response_code = 200001
    status_message = "PARAMETER_REQUIRED"


class ValidationParameterBlank(ValidationError):
    response_code = 200002
    status_message = "PARAMETER_MUST_NOT_BE_BLANK"


class ValidationParameterMaxLimit(ValidationError):
    response_code = 200003
    status_message = "PARAMETER_REACHES_THE_MAX_LENGTH"


class ValidationParameterMinLimit(ValidationError):
    response_code = 200004
    status_message = "PARAMETER_REACHES_THE_MIN_LENGTH"


class ValidationParameterInvalidEmail(ValidationError):
    response_code = 200005
    status_message = "INVALID_EMAIL_ADDRESS"


class ValidationParameterInvalidAlias(ValidationError):
    response_code = 200006
    status_message = "INVALID_ALIAS"


class ValidationParameterInvalidObjectType(ValidationError):
    response_code = 200006
    status_message = "INVALID_OBJECT_TYPE"


class ValidationParameterInvalidObjectId(ValidationError):
    response_code = 200007
    status_message = "INVALID_OBJECT_ID"


class ValidationParameterValueMin(ValidationError):
    response_code = 200008
    status_message = "PARAMETER_VALUE_TOO_SMALL"


class ValidationParameterValueMax(ValidationError):
    response_code = 200009
    status_message = "PARAMETER_VALUE_TOO_LARGE"


class ValidationParameterInvalid(ValidationError):
    response_code = 200010
    status_message = "PARAMETER_INVALID"



class ParamStructure(object):
    name = None
    type = None
    non_empty = True
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
        elif not self.value:
            return
        
        if self.type is not None:
            self._validate_type()
        
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

    def _validate_non_empty(self):
        if not bool(self.value) and self.value is not 0 \
        and self.value is not False:
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
    format_ObjectId = True
    def validator(self):
        if self.value and not ObjectId.is_valid(self.value):
            raise ValidationParameterInvalidObjectId(self.name)

class AliasStructure(ParamStructure):
    len_max = 100
    format_alias = True
    type = unicode
    def validator(self):
        alias_pattern = re.compile(r'^[a-z0-9_\-]+$')
        if not self.value or not alias_pattern.match(self.value.lower()):
            raise ValidationParameterInvalidAlias(self.name)

class IDStructure(ParamStructure):
    len_max = 500
    type = unicode
    
class SIDStructure(ParamStructure):
    len_max = 500
    type = unicode

class MD5Structure(ParamStructure):
    len_max = 32
    type = unicode

class TokenStructure(ParamStructure):
    len_max = 500
    type = unicode

class DictStructure(ParamStructure):
    type = dict

class AttrStructure(ParamStructure):
    len_max = 100
    type = unicode

class DescStructure(ParamStructure):
    len_max = 500
    type = unicode

class TextStructure(ParamStructure):
    len_max = 100000
    type = unicode

class ListStructure(ParamStructure):
    type = list

class FilenameStructure(ParamStructure):
    len_max = 200
    type = None

class FileStructure(ParamStructure):
    type = None

class IntegerStructure(ParamStructure):
    type = int

class BoolStructure(ParamStructure):
    type = bool

class UrlStructure(ParamStructure):
    len_max = 1000
    type = unicode

class ProtocolStructure(ParamStructure):
    len_max = 10
    type = unicode

class DomainStructure(ParamStructure):
    len_max = 100
    type = unicode

class EmailStructure(ParamStructure):
    len_max = 150
    type = unicode
    def validator(self):
        if not self.value or '@' not in self.value:
            raise ValidationParameterInvalidEmail(self.name)
        
class FlagBitStructure(ParamStructure):
    value_min = 0
    value_max = 100
    type = int
    
class LoginStructure(ParamStructure):
    len_max = 200
    type = unicode
    
class PasswordStructure(ParamStructure):
    len_max = 50
    type = unicode


# structure object
class Struct(object):

    Pwd = PasswordStructure
    Login = LoginStructure
    Email = EmailStructure
    Domain = DomainStructure
    Protocol = ProtocolStructure
    Url = UrlStructure
    Text = TextStructure
    Desc = DescStructure
    Attr = AttrStructure
    Token = TokenStructure
    Sid = SIDStructure
    Id = IDStructure
    MD5 = MD5Structure
    ObjectId = ObjectIdStructure
    Alias = AliasStructure
    
    Dict = DictStructure
    Bool = BoolStructure
    Flag = FlagBitStructure
    Int = IntegerStructure
    List = ListStructure
    
    File = FileStructure
    Filename = FilenameStructure
    