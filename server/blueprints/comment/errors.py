# coding=utf-8
from __future__ import absolute_import

from apiresps.errors import (InternalServerError,
                             NotFound)


class CommentExtentionError(InternalServerError):
    status_message = "COMMENT_EXTENTION_ERROR"
    response_code = 400001


class CommentGroupError(InternalServerError):
    status_message = "COMMENT_GROUP_ERROR"
    response_code = 400011


class CommentGroupNotFound(NotFound):
    status_message = "COMMENT_GROUP_NOT_FOUND"
    response_code = 400012


class CommentGroupKeyHasExsited(InternalServerError):
    status_message = "COMMENT_GROUPKEY_HAS_EXSITED"
    response_code = 400013


class CommentError(InternalServerError):
    status_message = "COMMENT_ERROR"
    response_code = 400021


class CommentNotFound(NotFound):
    status_message = "COMMENT_NOT_FOUND"
    response_code = 400022

class CommentNotAuthor(NotFound):
    status_message = "COMMENT_NOT_AUTHOR"
    response_code = 400022