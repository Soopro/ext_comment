# coding=utf-8
from __future__ import absolute_import

from bson import ObjectId
from mongokit import INDEX_DESCENDING
from utils.models import BaseDocument
from utils.base_utils import now


class CommentExtension(BaseDocument):
    structure = {
        'open_id' : unicode,
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
            "open_id" : open_id
        })


class CommentGroup(BaseDocument):
    structure = {
        'extension_id': ObjectId,
        'group_key': unicode,
        'update': int,
        'creation': int
    }

    use_dot_notation = True

    default_values = {
        'creation': now(),
        'update': now()
    }

    def find_one_by_group_key_and_eid(self, group_key, extension_id):
        return self.find_one({
            'group_key': group_key,
            'extension_id': ObjectId(extension_id)
        })

    def find_all_by_eid(self, extension_id):
        return self.find({
            'extension_id': ObjectId(extension_id)
        })


class Comment(BaseDocument):
    structure = {
        'creation': int,
        'content': unicode,
        'author_id': unicode,
        'author_name': unicode,
        'extension_id': ObjectId,
        'group_id': ObjectId,
        'group_key': unicode
    }

    use_dot_notation = True
    required_fields = ['content', 'author_name', 'extension_id', 'group_id']
    default_values = {'creation': now(),
                      'author_name': u'anonymous'}

    def find_one_by_id_and_gid_and_eid(self, 
        comment_id, group_id, extension_id):
        return self.find_one({
            '_id': ObjectId(comment_id),
            'group_id': ObjectId(group_id),
            'extension_id': ObjectId(extension_id)
        })

    def find_all_by_gid_and_eid(self, gid, extension_id):
        return self.find({
            'group_id': ObjectId(gid),
            'extension_id': ObjectId(extension_id)
        })

    def find_all_by_gkey_and_aid_desc(self, group_key, author_id, limit):
        return self.find({
            'group_key': group_key,
            'author_id': author_id
        }).sort('creation', INDEX_DESCENDING).limit(limit)
