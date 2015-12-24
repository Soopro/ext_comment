# coding=utf-8
from __future__ import absolute_import

from errors.base_errors import APIError


class CommentExtentionError(APIError):
    response_code = 0100
    

class CommentGroupError(APIError):
    response_code = 0200
    

class CommentGroupNotFound(CommentGroupError):
    response_code = 0210
    affix_message = "Group Not Found."
    

class CommentGroupKeyIsExsited(APIError):
    response_code = 0220
    affix_message = "Group key is existed."
    
    
class CommentError(APIError):
    response_code = 0300
    
    
class CommentNotFound(CommentError):
    response_code = 0310
    affix_message = "Comment Not Found."

    

