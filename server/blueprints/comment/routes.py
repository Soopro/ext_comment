# coding=utf-8
from __future__ import absolute_import

from .controllers import *

urls = [
    # open api
    ("/visit/group/<group_key>", visit_get_group_comments, "GET"),
    ("/visit/group/<group_key>", visit_add_comment, "POST"),
    ("/visit/group/<group_key>/<comment_id>", visit_remove_comment, "DELETE"),

    # admin api
    # ("/admin/extension", admin_add_comment_extension, "POST"),
    ("/admin/extension", admin_get_comment_extension, "GET"),
    ("/admin/extension", admin_update_comment_extension, "POST"),
    ("/admin/group", admin_list_comment_groups, "GET"),
    ("/admin/group/<group_key>", admin_get_group_comments, "GET"),
    ("/admin/group/<group_key>", admin_remove_batch_comments, "DELETE"),
    # ("/admin/group/<group_key>/<comment_id>", remove_comment, "DELETE")
]