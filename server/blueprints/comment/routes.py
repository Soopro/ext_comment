# coding=utf-8
from __future__ import absolute_import

from .controllers import *

urls = [
    # open api
    ("/visit/group/<group_key>/comment", visit_get_group_comments, "GET"),
    ("/visit/group/<group_key>/comment", visit_add_comment, "POST"),
    ("/visit/group/<group_key>/comment/<comment_id>", 
        visit_remove_comment, "DELETE"),

    # admin api
    # ("/admin/extension", admin_add_comment_extension, "POST"),
    ("/admin/extension", admin_get_comment_extension, "GET"),
    ("/admin/extension", admin_update_comment_extension, "POST"),
    ("/admin/group", admin_list_comment_groups, "GET"),
    # ("/admin/group", admin_add_comment_group, "POST"),
    ("/admin/group/<group_id>", admin_remove_group, "DELETE"),
    ("/admin/group/<group_id>/comment", admin_get_group_comments, "GET"),
    ("/admin/group/<group_id>/comment/batch", admin_remove_comments, "POST"),
    ("/admin/group/<group_id>/comment/<comment_id>", 
        admin_remove_comment, "DELETE"),
    # ("/admin/group/<group_key>/<comment_id>", remove_comment, "DELETE")
]