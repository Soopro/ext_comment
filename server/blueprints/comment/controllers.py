#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import current_app, request
from utils.base_utils import output_json, now, get_allowed_origin
from utils.request_json import get_request_json
from errors.validation_errors import ContentStructure
from errors.general_errors import (PermissionDenied, ErrCommentDeletionError,
                                   CommentGroupNotFound)
import base64
from errors.bp_users_errors import SooproAPIError


@output_json
def sync_comment_extension():
    data = request.get_json()
    User = current_app.mongodb_conn.User
    if data['status'] == User.STATUS_INACTIVATED:
        try:
            allowed_origin = get_allowed_origin(data['open_id'])
        except:
            raise SooproAPIError
        comment_ext = current_app.mongodb_conn.CommentExtension()
        comment_ext['allowed_origin'] = allowed_origin
        user = User.find_one_by_open_id(data['open_id'])
        user['status'] = User.STATUS_ACTIVATED
        return comment_ext
    elif data['status'] == User.STATUS_ACTIVATED:
        comment_ext = current_app.mongodb_conn.\
            CommentExtension.find_one_by_open_id(data['open_id'])
        comment_ext['allowed_origins'] = data['allowed_origins']
        comment_ext['title'] = data['title']
        comment_ext['style'] = data['style']
        comment_ext['thumbnail'] = data['thumbnail']
        comment_ext['require_login'] = data['require_login']
        comment_ext.save()
        return {'status': 'OK'}
    else:
        raise PermissionDenied





@output_json
def get_comment_extension():
    open_id = request.get_json('open_id')
    try:
        comment_ext = current_app.mongodb_conn. \
            CommentExtension.find_one_by_open_id(open_id)
    except:
        raise PermissionDenied
    return comment_ext


@output_json
def add_comment(group_key):
    # auth
    # domain
    # member (option) member_token, open_id

    remote_addr = unicode(request.remote_addr)
    user_agent = unicode(request.headers.get('User-Agent'))

    # if user is anonymous
    author_id = u"{}{}".format(remote_addr, user_agent)
    ext_id = base64.b64decode(request.headers.get('ExtKey'))
    comment_ext = current_app.mongodb_conn. \
        CommentExtension.find_one_by_eid(ext_id)
    comments = list(current_app.mongodb_conn. \
                    Comment.find_by_eid_and_aid_desc(comment_ext, author_id))

    if comments is not None:
        if len(comments) == 5:
            time_diff = now() - comments[-1].creation
            if time_diff < 3600:
                raise PermissionDenied("Please wait for a while to post")

    content = get_request_json('content', validator=ContentStructure,
                               required=True)
    comment_group = current_app.mongodb_conn. \
        CommentGroup.find_one_by_group_key(group_key)
    if comment_group is None:
        comment_group = current_app.mongodb_conn.CommentGroup()
        comment_group.ext_id = ext_id
        comment_group.group_key = unicode(group_key)
        comment_group.save()
    comment = current_app.mongodb_conn.Comment()
    comment.content = content
    comment.author_id = author_id
    comment.ext_id = ext_id
    comment.group_id = comment_group._id
    comment.group_key = unicode(group_key)
    comment.save()

    return comment


@output_json
def remove_comment(group_key, comment_id):
    comment_group = current_app.mongodb_conn. \
        CommentGroup.find_one_by_group_key(group_key)
    try:
        comment = current_app.mongodb_conn. \
            Comment.find_one_by_gid(comment_group._id)
        comment.delete()
    except:
        raise ErrCommentDeletionError
    return {'id': comment_id,
            'status': 'deleted successfully'}


@output_json
def remove_batch_comments(group_key):
    comment_group = current_app.mongodb_conn. \
        CommentGroup.find_one_by_group_key(group_key)
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
def list_comment_groups():
    ext_id = base64.b64decode(request.headers.get('ExtKey'))
    comment_groups = list(current_app.mongodb_conn. \
                          CommentGroup.find_all_by_eid(ext_id))

    return comment_groups


@output_json
def get_group_comments(group_key):
    try:
        comment_group = current_app.mongodb_conn. \
            CommentGroup.find_one_by_group_key(group_key)
    except:
        raise CommentGroupNotFound
    list_comments = list(current_app.mongodb_conn. \
                         Comment.find_all_by_gid(comment_group._id))
    return list_comments
