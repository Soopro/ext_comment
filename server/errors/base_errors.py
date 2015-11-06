#coding=utf-8
from __future__ import absolute_import

import httplib


class Meta(type):
    def __init__(cls, clsname, bases, attrs):
        super(Meta, cls).__init__(clsname, bases, attrs)
        if 'response_code' not in attrs:
            # print cls, cls.status_code
            cls.response_code = getattr(cls, 'status_code')


class APIError(Exception):
    """
    Base class for all api exceptions.
    Subclasses should provide 'code' and 'message' properties.
    """
    __metaclass__ = Meta
    status_code = httplib.INTERNAL_SERVER_ERROR
    response_code = 0
    status_message = 'error'
    affix_message = None

    def __init__(self, message=None):
        self.affix_message = message

    def __str__(self):
        return '{}:{}'.format(self.status_message, self.affix_message)