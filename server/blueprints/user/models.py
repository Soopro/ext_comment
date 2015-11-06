# coding=utf-8
from __future__ import absolute_import

from mongokit import Document


class User(Document):
    use_dot_notation = True
    __collection__ = 'users'

    structure = {
        "open_id": unicode,
        "alias": unicode,
        "access_token": unicode,
        "refresh_token": unicode,
        "token_type": unicode,
        "expires_in": int,
        "random_string": unicode
    }

    default_values = {
        "alias": None
    }

    def find_one_by_open_id(self, open_id):
        return self.find_one({
            "open_id": open_id
        })
