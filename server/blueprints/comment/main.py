# coding=utf-8
from __future__ import absolute_import

from .routes import urls
from flask import Blueprint, request
from errors.base_errors import APIError
from utils.verify import verify_outer, verify_token
from utils.base_utils import route_inject, make_json_response

bp_name = 'comment'

apis_for_visitors = [
    "{}.visit_get_group_comments".format(bp_name),
    "{}.visit_add_comment".format(bp_name),
    "{}.visit_remove_comment".format(bp_name)
]

apis_for_admins = [
    "{}.admin_add_comment_extension".format(bp_name),
    "{}.admin_get_comment_extension".format(bp_name),
    "{}.admin_update_comment_extension".format(bp_name),
    "{}.admin_list_comment_groups".format(bp_name),
    "{}.admin_get_group_comments".format(bp_name),
    "{}.admin_remove_batch_comments".format(bp_name)
]

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urls)


@blueprint.before_request
def before_request():
    if request.endpoint in apis_for_visitors:
        verify_outer()
    elif request.endpoint in apis_for_admins:
        verify_token()
    return


@blueprint.errorhandler(APIError)
def comment_api_err(error):
    return make_json_response(error)
