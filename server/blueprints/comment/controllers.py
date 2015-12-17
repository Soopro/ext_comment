# coding=utf-8
from __future__ import absolute_import

from flask import current_app, request
from utils.base_utils import output_json, now
from utils.comment_utils import get_allowed_origin
from utils.request_json import get_request_json
from errors.validation_errors import ContentStructure
from errors.general_errors import (PermissionDenied, ErrCommentDeletionError,
                                   CommentGroupNotFound)
import base64
from errors.bp_users_errors import SooproAPIError
    
    
# endpoints for visitors
@output_json
def visit_get_group_comments(group_key):
    comment_group = _get_comment_group(group_key)
    comments = current_app.mongodb_conn. \
         Comment.find_all_by_gid(comment_group['_id'])
    comments = [_output_comment(comment) for comment in comments]
    return comments
    
    
@output_json
def visit_add_comment(group_key):
    # auth
    # domain
    # member (option) member_token, open_id

    remote_addr = unicode(request.remote_addr)
    user_agent = unicode(request.headers.get('User-Agent'))
    author_id = u"{}{}".format(remote_addr, user_agent)
    
    comment_extension = _get_current_comment_extension()
    

    def limit_comments(max_comment, min_time):
        Comment = current_app.mongodb_conn.Comment
        comments = list(Comment.find_by_eid_and_aid_desc(
            comment_extension['_id'], author_id, MAXCOMMENTS))

        if comments and len(comments) == MAXCOMMENTS:
            time_diff = now() - comments[-1].creation
            if time_diff < MINTIME:
                raise PermissionDenied("Please wait for a while to post")
    
    limit_comments(5, 3600)

    comment_group = _get_comment_group(group_key)
    comment = current_app.mongodb_conn.Comment()
    comment.content = get_request_json('content', 
        validator=ContentStructure, required=True)
    comment.author_id = author_id
    comment.ext_id = ext_id
    comment.group_id = comment_group._id
    comment.group_key = unicode(group_key)
    comment.save()

    return _output_comment(comment)

    
@output_json
def visit_remove_comment(group_key, comment_id):
    comment = _get_comment(comment_id, group_key)
    return _output_comment(comment)
    

# endpoints for admins
# @output_json
# def admin_add_comment_extension():
#     comment_extension = _new_comment_extension()
#     comment_extension.save()
#     return _output_comment_extension(comment_extension)
    
    
@output_json
def admin_get_comment_extension():
    comment_extension = _get_current_comment_extension()
    return _output_comment_extension(comment_extension)
    
   
@output_json
def admin_update_comment_extension():
    data = request.get_json()
    comment_extension = _get_current_comment_extension()
    comment_ext['allowed_origins'] = data['allowed_origins']
    comment_ext['title'] = data['title']
    comment_ext['style'] = data['style']
    comment_ext['thumbnail'] = data['thumbnail']
    comment_ext['require_login'] = data['require_login']
    comment_ext.save()
    return _output_comment_extension(comment_extension)
    
    
@output_json
def admin_list_comment_groups():
    comment_extension = _get_current_comment_extension()
    comment_groups = current_app.mongodb_conn.\
        CommentGroup.find_all_by_eid(comment_extension['_id'])
    comment_groups = [_output_comment_group(group) for group in comment_groups]
    return comment_groups
    
    
@output_json
def admin_get_group_comments(group_key):
    comment_group = _get_comment_group(group_key)
    comments = current_app.mongodb_conn. \
         Comment.find_all_by_gid(comment_group['_id'])
    comments = [_output_comment(comment) for comment in comments]
    return comments
    
    
@output_json
def admin_remove_batch_comments(group_key):
    comment_group = _get_comment_group(group_key)
    comments = current_app.mongodb_conn. \
         Comment.find_all_by_gid(comment_group['_id'])
    for comment in comments:
        comment.delete()
    comment_group.delete()
    return _get_comment_group(comment_group)    
    

def _output_comment_extension(comment_extension):
    return {
        "title": comment_extension.title,
        "allowed_origins": comment_extension.allowed_origins,
        "style": comment_extension.style,
        "thumbnail": comment_extension.thumbnail,
        "require_login": comment_extension.require_login,
    }
    

def _output_comment_group(comment_group):
    pass


def _output_comment(comment):
    pass
    
    
# def _new_comment_extension():
#     CommentExtension = current_app.mongodb_conn.CommentExtension
#     comment_extension = CommentExtension.\
#         find_one_by_open_id(g.current_user["_id"])
#     if comment_extension:
#         raise ExtensionIsExisted()
#     comment_extension = CommentExtension()
#     comment_extension.user_id = g.current_user["_id"]
#     comment_extension.save()
#     return comment_extension
    
    
def _create_comment_extension():
    comment_extension = current_app.mongodb_conn.CommentExtension()
    comment_extension.user_id = g.current_user["_id"]
    comment_extension.save()
    return comment_extension
    
    
def _get_current_comment_extension():
    if g.current_user:
        comment_extension = current_app.mongodb_conn.\
            CommentExtension.find_one_by_open_id(g.current_user["_id"])
    else:
        comment_extension = g.current_comment_extension
    if not comment_extension:
        comment_extension = _create_comment_extension()
    return comment_extension
    
    
def _get_comment_group(group_key):    
    extension_id = _get_current_comment_extension().extension_id
    comment_group = current_app.mongodb_conn. \
        CommentGroup.find_one_by_group_key_and_eid(group_key, extension_id)
    if not comment_group:
        raise GroupNotFound()
    return comment_group
    
    
def _get_comment(comment_id, group_key):
    extension_id = _get_current_comment_extension().extension_id
    comment = current_app.mongodb_conn.Comment.\
        find_one_by_id_and_gid_and_eid(comment_id, group_key, extension_id)
    if not comment:
        raise CommentNotFound()
    return comment