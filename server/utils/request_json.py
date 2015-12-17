# coding=utf-8
from __future__ import absolute_import

from flask import request
from errors.general_errors import (ErrInvalidRequestBody,
                                     ErrRequestBodyNotExists)
from errors.validation_errors import ValidationParameterRequired


def _ensure_request(req_type):
    try:
        source = getattr(request, req_type)
    except Exception:
        raise ErrInvalidRequestBody    
    if source is None:
        raise ErrRequestBodyNotExists
    if not isinstance(source, dict):
        raise ErrInvalidRequestBody
    return source

def is_empty_value(value):
    return value != False and value != 0 and not bool(value)
    

def get_request_json(key, validator=None, default=None, required=False):
    source = _ensure_request('json')

    if required and key not in source:
        raise ValidationParameterRequired(key)
    
    value = source.get(key)
    
    if not isinstance(validator, list):
        validator = [validator]
    
    if is_empty_value(value):
        if default is not None:
            value = default
        elif required:
            raise ValidationParameterRequired(key)
        
    for vld in validator:
        if not hasattr(vld, '__call__'):
            continue
        vld(value, name=key)
    
    return value
    
