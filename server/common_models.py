# coding=utf-8
from __future__ import absolute_import

from mongokit import Document


class User(Document):
    __collection__ = 'users'

    STATUS_INACTIVATED = 0
    STATUS_ACTIVATED = 1

    use_dot_notation = True

    structure = {
        "open_id": unicode,
        "alias": unicode,
        "display_name": unicode,
        "access_token": unicode,
        "refresh_token": unicode,
        "token_type": unicode,
        "expires_in": int,
        "random_string": unicode,
        "ext_token": unicode,
        "status": int,
    }

    default_values = {
        "alias": u'',
        "display_name": u'',
        "expires_in": 0,
        "status": STATUS_INACTIVATED,
    }

    def find_one_by_open_id(self, open_id):
        return self.find_one({
            "open_id": open_id
        })
