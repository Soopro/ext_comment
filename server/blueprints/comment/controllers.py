# coding=utf-8
from __future__ import absolute_import

from flask import current_app, request, g
from utils.api_utils import output_json
from utils.helpers import now
from utils.request import get_param
from .errors import (CommentGroupKeyHasExsited,
                     CommentGroupNotFound,
                     CommentNotFound)


# endpoints for visitors
@output_json
def visit_get_group_comments(group_key):
    comments = _visit_get_comments(group_key)

    return [output_comment(comment) for comment in comments]


@output_json
def visit_add_comment(group_key):
    # auth
    # domain
    # member (option) member_token, open_id

    remote_addr = unicode(request.remote_addr)
    user_agent = unicode(request.headers.get('User-Agent'))
    author_id = u"{} - {}".format(remote_addr, user_agent)
    # print author_id
    comment_extension = _get_current_comment_extension()

    def limit_comments(max_comment, min_time):
        Comment = current_app.mongodb_conn.Comment
        comments = list(Comment.find_by_gkey_and_eid_and_aid_desc(
            group_key, comment_extension['_id'], author_id, max_comment))

        if comments and len(comments) == max_comment:
            time_diff = now() - comments[-1].creation
            if time_diff < min_time:
                raise PermissionDenied("Please wait for a while to post")

    limit_comments(5, 3600)

    content = request.get_json()['content']

    comment_group = _visit_get_comment_group(group_key)

    comment = current_app.mongodb_conn.Comment()
    comment.content = content
    comment.author_id = author_id
    comment.extension_id = comment_extension['_id']
    comment.group_id = comment_group['_id']
    comment.group_key = unicode(group_key)
    comment.save()

    return output_comment(comment)


@output_json
def visit_remove_comment(group_key, comment_id):
    comment = _visit_get_comment(comment_id, group_key)

    return output_comment(comment)


# endpoints for admins
# @output_json
# def admin_add_comment_extension():
#     comment_extension = _new_comment_extension()
#     comment_extension.save()
#     return output_comment_extension(comment_extension)


@output_json
def admin_get_comment_extension():
    comment_extension = _get_current_comment_extension()

    return output_comment_extension(comment_extension)


@output_json
def admin_update_comment_extension():
    allowed_origins = get_param('allowed_origins', )
    title = get_param('title', )
    style = get_param('style', )
    thumbnail = get_param('thumbnail', )
    require_login = get_param('require_login', )

    # print data
    comment_extension = _get_current_comment_extension()
    comment_extension['allowed_origins'] = allowed_origins
    comment_extension['title'] = title
    comment_extension['style'] = style
    comment_extension['thumbnail'] = thumbnail
    comment_extension['require_login'] = require_login
    comment_extension.save()

    return output_comment_extension(comment_extension)


@output_json
def admin_list_comment_groups():
    comment_groups = _get_comment_groups()
    return [output_comment_group(group) for group in comment_groups]


# @output_json
# def admin_add_comment_group():
#     data = request.get_json()
#     group_key = data["group_key"]
#     comment_group = _create_comment_group(group_key)
#     return output_comment_group(comment_group)


@output_json
def admin_remove_group(group_id):
    comment_group = _admin_get_comment_group(group_id)
    comments = _admin_get_comments(group_id)
    for comment in comments:
        comment.delete()
    comment_group.delete()

    return output_comment_group(comment_group)


@output_json
def admin_get_group_comments(group_id):
    comments = _admin_get_comments(group_id)

    return [output_comment(comment) for comment in comments]


@output_json
def admin_remove_comment(group_id, comment_id):
    comment = _admin_get_comment(comment_id, group_id)
    comment.delete()

    return output_comment(comment)


@output_json
def admin_remove_comments(group_id):
    def deal_comments(comment_id, group_id):
        comment = _admin_get_comment(comment_id, group_id)
        comment.delete()
        return output_comment(comment)

    comment_ids = get_param('comment_ids', )

    return {
        "deleted": [deal_comments(comment_id, group_id)
                    for comment_id in comment_ids]
    }


def output_comment_extension(comment_extension):
    return {
        "title": comment_extension['title'],
        "allowed_origins": comment_extension['allowed_origins'],
        "style": comment_extension['style'],
        "thumbnail": comment_extension['thumbnail'],
        "require_login": comment_extension['require_login'],
    }


def output_comment_group(comment_group):
    return {
        "id": comment_group['_id'],
        "group_key": comment_group['key'],
        "update": comment_group['update']
    }


def output_comment(comment):
    return {
        'id': comment['_id'],
        'author_name': comment['author_name'],
        'creation': comment['creation'],
        'content': comment['content']
    }


# def _new_comment_extension():
#     CommentExtension = current_app.mongodb_conn.CommentExtension
#     comment_extension = CommentExtension.\
#         find_one_by_open_id(g.curr_user["_id"])
#     if comment_extension:
#         raise ExtensionIsExisted()
#     comment_extension = CommentExtension()
#     comment_extension.user_id = g.curr_user["_id"]
#     comment_extension.save()
#     return comment_extension


def _create_comment_extension():
    comment_extension = current_app.mongodb_conn.CommentExtension()
    comment_extension.open_id = g.curr_user.open_id
    comment_extension.save()
    return comment_extension


def _get_current_comment_extension():
    # print g.curr_user
    if hasattr(g, 'current_comment_extension'):
        comment_extension = g.current_comment_extension
    elif hasattr(g, 'curr_user'):
        comment_extension = current_app.mongodb_conn.\
            CommentExtension.find_one_by_open_id(g.curr_user.open_id)
        if not comment_extension:
            comment_extension = _create_comment_extension()
        g.current_comment_extension = comment_extension
    return comment_extension


def _create_comment_group(group_key):
    comment_extension = _get_current_comment_extension()
    CommentGroup = current_app.mongodb_conn.CommentGroup
    if CommentGroup.find_one_by_gid_and_eid(group_key, comment_extension._id):
        raise CommentGroupKeyHasExsited()
    comment_group = CommentGroup()
    comment_group.group_key = group_key
    comment_group.extension_id = comment_extension._id
    comment_group.save()
    return comment_group


def _get_comment_groups():
    comment_extension = _get_current_comment_extension()
    comment_groups = current_app.mongodb_conn.\
        CommentGroup.find_all_by_eid(comment_extension['_id'])
    return comment_groups


def _visit_get_comment_group(group_key):
    comment_extension = _get_current_comment_extension()
    comment_group = current_app.mongodb_conn. \
        CommentGroup.find_one_by_gkey_and_eid(group_key,
                                              comment_extension['_id'])
    if not comment_group:
        comment_group = _create_comment_group(group_key)
    return comment_group


def _visit_get_comment(comment_id, group_key):
    comment_extension = _get_current_comment_extension()
    comment = current_app.mongodb_conn.Comment.\
        find_one_by_id_and_gkey_and_eid(comment_id,
                                        group_key, comment_extension['_id'])
    if not comment:
        raise CommentNotFound()
    return comment


def _visit_get_comments(group_key):
    comment_extension = _get_current_comment_extension()
    comments = current_app.mongodb_conn.Comment.\
        find_all_by_gkey_and_eid(group_key, comment_extension['_id'])
    return comments


def _admin_get_comment_group(group_id):
    comment_extension = _get_current_comment_extension()
    comment_group = current_app.mongodb_conn. \
        CommentGroup.find_one_by_gid_and_eid(group_id,
                                             comment_extension['_id'])
    if not comment_group:
        raise CommentGroupNotFound()
    return comment_group


def _admin_get_comment(comment_id, group_id):
    comment_extension = _get_current_comment_extension()
    comment = current_app.mongodb_conn.Comment.\
        find_one_by_id_and_gid_and_eid(comment_id,
                                       group_id, comment_extension['_id'])
    if not comment:
        raise CommentNotFound()
    return comment


def _admin_get_comments(group_id):
    comment_extension = _get_current_comment_extension()
    comments = current_app.mongodb_conn.Comment.\
        find_all_by_gid_and_eid(group_id, comment_extension['_id'])
    return comments
