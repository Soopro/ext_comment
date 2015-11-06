#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from bson import ObjectId
from mongokit import INDEX_DESCENDING
from utils.models import BaseDocument
from utils.base_utils import now


class CommentExtension(BaseDocument):
    structure = {
        'app_id': ObjectId,
        'allowed_origins': unicode
    }

    use_dot_notation = True

    def find_one_by_eid(self, ext_id):
        return self.find_one({
            "_id": ObjectId(ext_id)
        })


class CommentGroup(BaseDocument):
    structure = {
        'ext_id': ObjectId,
        'group_name': unicode
    }

    use_dot_notation = True

    def find_one_by_eid_and_gname(self, ext_id, group_name):
        return self.find_one({
            'ext_id': ObjectId(ext_id),
            'group_name': group_name
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
        'group_id': ObjectId
    }

    use_dot_notation = True
    required_fields = ['content', 'author_name', 'ext_id', 'group_id']
    default_values = {'creation': now(),
                      'author_name': u'anonymous'}

    def find_one_by_id(self, comment_id):
        return self.find_one({
            '_id': ObjectId(comment_id)
        })

    def find_all_by_gid(self, group_id):
        return self.find({
            'group_id': ObjectId(group_id)
        })

    def find_by_eid_and_aid_desc(self, author_id, ext_id):
        return self.find({
            'author_id': author_id,
            'ext_id': ext_id
        }).sort('creation', INDEX_DESCENDING).limit(5)
