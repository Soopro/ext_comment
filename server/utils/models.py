# coding=utf-8
from __future__ import absolute_import

from mongokit import Document
from mongokit.document import DocumentProperties
from inflection import underscore, pluralize

import time


class MetaDoc(DocumentProperties):

    def __init__(cls, name, bases, attrs):
        super(MetaDoc, cls).__init__(name, bases, attrs)
        if not name.startswith('Callable'):
            if '__collection__' not in cls.__dict__:
                cls.__collection__ = pluralize(underscore(cls.__name__))
        return


class BaseDocument(Document):
    __metaclass__ = MetaDoc
    use_schemaless = False

    def save(self, *args, **kwargs):
        if 'updated' in self:
            self['updated'] = int(time.time())
        return super(BaseDocument, self).save(*args, **kwargs)

    def sly_save(self, *args, **kwargs):
        return super(BaseDocument, self).save(*args, **kwargs)
