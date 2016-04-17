# coding=utf-8
from __future__ import absolute_import

from mongokit import Document
from utils.helpers import now


class ExtUser(Document):
    __collection__ = 'ext_users'

    STATUS_INACTIVATED = 0
    STATUS_ACTIVATED = 1

    structure = {
        "open_id": unicode,
        "scope": unicode,
        "display_name": unicode,
        "title": unicode,
        "locale": unicode,
        "description": unicode,
        "type": unicode,
        "snapshot": unicode,
        "access_token": unicode,
        "refresh_token": unicode,
        "token_type": unicode,
        "expires_at": int,
        "status": int,
        "updated": int,
        "creation": int,
    }

    required_fields = ["open_id"]

    default_values = {
        "scope": u'',
        "title": u'',
        "locale": u'',
        "description": u'',
        "type": u'',
        "snapshot": u'',
        "access_token": u'',
        "refresh_token": u'',
        "token_type": u'',
        "expires_at": 0,
        "status": STATUS_INACTIVATED,
        "updated": now,
        "creation": now,
    }
    indexes = [
        {
            'fields': ['open_id'],
            'unique': True,
        },
    ]

    def find_one_by_open_id(self, open_id):
        return self.find_one({
            "open_id": open_id
        })

    def find_one_activated_by_open_id(self, open_id):
        return self.find_one({
            "open_id": open_id,
            "status": self.STATUS_ACTIVATED,
        })

    def save(self, *args, **kwargs):
        self['updated'] = now()
        return super(ExtUser, self).save(*args, **kwargs)
