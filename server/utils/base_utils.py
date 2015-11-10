from __future__ import absolute_import

from functools import wraps
from .response_json import _content_data, make_json_response, STATUS_OK
import time
from flask import request, current_app
from errors.general_errors import (PermissionDenied,
                                   ExtensionNotFound)
import base64

def route_inject(app_or_blueprint, url_patterns):
    for pattern in url_patterns:
        options = pattern[3] if len(pattern) > 3 else {}
        app_or_blueprint.add_url_rule(pattern[0],
                                      view_func=pattern[1],
                                      methods=pattern[2].split(),
                                      **options)


def now():
    return int(time.time())


def output_json(f):
    @wraps(f)
    def decorate(*args, **kwargs):
        result = f(*args, **kwargs)
        data = _content_data(result)
        return make_json_response(STATUS_OK, data)

    return decorate


def verify_outer():
    ExtKey = request.headers.get('ExtKey')
    ext_id = base64.b64decode(ExtKey)
    try:
        comment_ext = current_app.mongodb_conn.\
                CommentExtension.find_one_by_eid(ext_id)
    except:
        raise ExtensionNotFound
    if request.url.startswith(comment_ext.allowed_origin) is False:
        raise PermissionDenied

    if comment_ext.get("require_login"):
        memeber_token = request.headers.get('MemberAuthr')
        open_id = comment_ext["open_id"]
        # TODO: Check member token
        # raise PermissionDenied
    return


