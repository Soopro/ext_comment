#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import current_app, request, g
from utils.base_utils import output_json
from utils.request_json import get_request_json
from errors.validation_errors import ContentStructure
from errors.general_errors import (PermissionDenied, ErrCommentDeletionError,
                                   CommentGroupNotFound)
from utils.base_utils import now
from bson import ObjectId


@output_json
def get_comment_extension():




@output_json
def add_comment(ext_id, group_name):
    # auth
    # domain
    # member (option) member_token, open_id

    remote_addr = unicode(request.remote_addr)
    user_agent = unicode(request.headers.get('User-Agent'))
    author_id = u"{}{}".format(remote_addr, user_agent)

    comments = list(current_app.mongodb_conn. \
                    Comment.find_by_eid_and_aid_desc(ext_id, author_id))

    if comments is not None:
        if len(comments) == 5:
            time_diff = now() - comments[-1].creation
            if time_diff < 3600:
                raise PermissionDenied("Please wait for a while to post")

    content = get_request_json('content', validator=ContentStructure,
                               required=True)
    comment_group = current_app.mongodb_conn. \
        CommentGroup.find_one_by_eid_and_gname(ext_id, group_name)
    if comment_group is None:
        comment_group = current_app.mongodb_conn.CommentGroup()
        comment_group.ext_id = ObjectId(ext_id)
        comment_group.group_name = unicode(group_name)
        comment_group.save()
    comment = current_app.mongodb_conn.Comment()
    comment.content = content
    comment.author_id = author_id
    comment.ext_id = ObjectId(ext_id)
    comment.group_id = comment_group._id
    comment.save()

    return comment


@output_json
def remove_comment(ext_id, group_name, comment_id):
    try:
        comment = current_app.mongodb_conn.Comment.find_one_by_id(comment_id)
        comment.delete()
    except:
        raise ErrCommentDeletionError

    return {'id': comment_id,
            'status': 'deleted successfully'}


@output_json
def remove_batch_comments(ext_id, group_name):
    comment_group = current_app.mongodb_conn. \
        CommentGroup.find_one_by_eid_and_gname(ext_id, group_name)
    try:
        comments = current_app.mongodb_conn. \
            Comment.find_all_by_gid(comment_group._id)
        for comment in comments:
            comment.delete()
        comment_group.delete()
    except:
        raise ErrCommentDeletionError

    message = {"status": "comments deleted successfully"}

    return message


@output_json
def list_comment_groups(ext_id):
    comment_groups = list(current_app.mongodb_conn. \
                          CommentGroup.find_all_by_eid(ext_id))

    return comment_groups


@output_json
def list_comments(ext_id, group_name):
    try:
        comment_group = current_app.mongodb_conn. \
            CommentGroup.find_one_by_eid_and_gname(ext_id, group_name)
    except:
        raise CommentGroupNotFound
    list_comments = list(current_app.mongodb_conn. \
                         Comment.find_all_by_gid(comment_group._id))
    return list_comments
