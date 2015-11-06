from __future__ import absolute_import

from .controllers import *

urls = [
    # open api
    ("/visit/group/<group_key>", list_comments, "GET"),
    ("/visit/group/<group_key>", add_comment, "POST"),
    ("/visit/group/<group_key>/<comment_id>", remove_comment, "DELETE"),

    # admin api
    ("/manage/group", list_comment_groups, "GET"),
    ("/manage/group/<group_key>", get_group_comments, "GET"),
    ("/manage/group/<group_key>", remove_batch_comments, "DELETE"),
    ("/manage/group/<group_key>/<comment_id>", remove_comment, "DELETE"),
    ("/manage/settings", get_comment_extension, "GET"),
    ]