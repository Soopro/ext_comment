# coding=utf-8
from __future__ import absolute_import

from bson import ObjectId
from mongokit import INDEX_DESCENDING
from utils.models import BaseDocument
from utils.base_utils import now


class CommentExtension(BaseDocument):
    structure = {
        'user_id' : ObjectId,
        'allowed_origins': unicode,
        'title' : unicode,
        'style' : unicode,
        'thumbnail' : unicode,
        'require_login' : bool
    }

    use_dot_notation = True

    required_fields = ['open_id']

    default_values = {
        'allowed_origins': u'',
        'title': u'',
        'style': u'',
        'thumbnail': u'',
        'require_login': False
    }

    def find_one_by_eid(self, ext_id):
        return self.find_one({
            "_id": ObjectId(ext_id)
        })

    def find_one_by_open_id(self, open_id):
        return self.find_one({
            "open_id" : ObjectId(open_id)
        })


class CommentGroup(BaseDocument):
    structure = {
        'ext_id': ObjectId,
        'group_key': unicode,
        'creation': int
    }

    use_dot_notation = True

    default_values = {'creation': now()}

    def find_one_by_group_key(self, group_key):
        return self.find_one({
            'group_key': group_key
        })

    def find_all_by_eid(self, ext_id):
        return self.find({
            'ext_id': ObjectId(ext_id)
        })


class Comment(BaseDocument):
    structure = {
        'creation': int,
        'content': unicode,
        'author_id': unicode,
        'author_name': unicode,
        'ext_id': ObjectId,
        'group_id': ObjectId,
        'group_key': unicode
    }

    use_dot_notation = True
    required_fields = ['content', 'author_name', 'ext_id', 'group_id']
    default_values = {'creation': now(),
                      'author_name': u'anonymous'}

    def find_one_by_id(self, comment_id):
        return self.find_one({
            '_id': ObjectId(comment_id)
        })

    def find_all_by_gid(self, gid):
        return self.find({
            'group_id': ObjectId(gid)
        })

    def find_by_gkey_and_aid_desc(self, group_key, author_id):
        return self.find({
            'author_id': author_id,
            'group_key': group_key
        }).sort('creation', INDEX_DESCENDING).limit(5)
