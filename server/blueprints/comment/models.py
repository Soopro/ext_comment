# coding=utf-8
from __future__ import absolute_import

from bson import ObjectId
from mongokit import INDEX_DESCENDING
from utils.models import BaseDocument
from utils.helpers import now


class CommentExtension(BaseDocument):
    __collection__ = 'comment_extensions'

    structure = {
        'open_id': unicode,
        'allowed_origins': unicode,
        'title': unicode,
        'style': unicode,
        'thumbnail': unicode,
        'require_login': bool,
        'updated': int,
        'creation': int,
    }

    use_dot_notation = True

    required_fields = ['open_id']

    default_values = {
        'allowed_origins': u'',
        'title': u'',
        'style': u'',
        'thumbnail': u'',
        'require_login': False,
        'creation': now,
        'updated': now,
    }

    def find_one_by_eid(self, ext_id):
        return self.find_one({
            "_id": ObjectId(ext_id)
        })

    def find_one_by_open_id(self, open_id):
        return self.find_one({
            "open_id": open_id
        })


class CommentGroup(BaseDocument):
    __collection__ = 'comment_groups'

    structure = {
        'extension_id': ObjectId,
        'key': unicode,
        'updated': int,
        'creation': int
    }

    use_dot_notation = True

    default_values = {
        'creation': now,
        'updated': now,
    }

    def find_one_by_gkey_eid(self, group_key, extension_id):
        return self.find_one({
            'group_key': group_key,
            'extension_id': ObjectId(extension_id)
        })

    def find_one_by_gid_eid(self, group_id, extension_id):
        return self.find_one({
            '_id': ObjectId(group_id),
            'extension_id': ObjectId(extension_id)
        })


    def find_all_by_eid(self, extension_id):
        return self.find({
            'extension_id': ObjectId(extension_id)
        })


class Comment(BaseDocument):
    __collection__ = 'comments'

    structure = {
        'creation': int,
        'content': unicode,
        'author_id': unicode,
        'meta': dict,
        'extension_id': ObjectId,
        'group_id': ObjectId,
        'group_key': unicode,
        'creation': int,
        'updated': int,
    }

    use_dot_notation = True
    required_fields = ['content', 'extension_id', 'group_id']
    default_values = {
        'meta': {},
        'creation': now,
        'updated': now,
    }

    def find_one_by_id_gid_eid(self, comment_id, group_id, extension_id):
        return self.find_one({
            '_id': ObjectId(comment_id),
            'group_id': ObjectId(group_id),
            'extension_id': ObjectId(extension_id)
        })

    def find_one_by_id_gkey_eid(self, comment_id, group_key, extension_id):
        return self.find_one({
            '_id': ObjectId(comment_id),
            'group_key': group_key,
            'extension_id': ObjectId(extension_id)
        })

    def find_all_by_gid_eid(self, group_id, extension_id):
        return self.find({
            'group_id': ObjectId(group_id),
            'extension_id': ObjectId(extension_id)
        })

    def find_all_by_gkey_eid(self, group_key, extension_id):
        return self.find({
            'group_key': group_key,
            'extension_id': ObjectId(extension_id)
        })

    def find_by_gkey_eid_aid(self, group_key, extension_id, author_id, limit):
        return self.find({
            'group_key': group_key,
            'extension_id': extension_id,
            'author_id': author_id
        }).sort('creation', INDEX_DESCENDING).limit(limit)
