# coding=utf-8
from __future__ import absolute_import

from .routes import urls
from flask import Blueprint, request, current_app
from apiresps import APIError
from ..helpers import verify_outer, verify_token
from utils.helpers import route_inject
from utils.api_utils import make_json_response

bp_name = 'comment'

apis_for_visitors = [
    "{}.visit_get_group_comments".format(bp_name),
    "{}.visit_get_comment".format(bp_name),
    "{}.visit_add_comment".format(bp_name),
    "{}.visit_remove_comment".format(bp_name)
]

apis_for_admins = [
    # "{}.admin_add_comment_extension".format(bp_name),
    "{}.admin_get_comment_extension".format(bp_name),
    "{}.admin_update_comment_extension".format(bp_name),
    "{}.admin_list_comment_groups".format(bp_name),
    "{}.admin_remove_group".format(bp_name),
    "{}.admin_get_group_comments".format(bp_name),
    "{}.admin_remove_comment".format(bp_name),
    "{}.admin_remove_comments".format(bp_name)
]

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urls)


@blueprint.before_app_first_request
def before_first_request():
    from .models import (Comment, CommentGroup, CommentExtension)
    current_app.mongodb_database.register([
        Comment, CommentGroup, CommentExtension])


@blueprint.before_request
def before_request():
    if request.endpoint in apis_for_visitors:
        verify_outer()
    elif request.endpoint in apis_for_admins:
        verify_token()


@blueprint.errorhandler(APIError)
def comment_api_err(error):
    print error
    return make_json_response(error)
