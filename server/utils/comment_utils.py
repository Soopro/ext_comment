
from flask import request, current_app, json
import base64
import requests
from errors.general_errors import ExtensionNotFound, PermissionDenied


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


def get_allowed_origin(open_id):
    payloads = {
        'open_id': open_id
    }
    headers = {'content-type': 'application/json'}
    r = requests.post(current_app.config.get(''),
                    # TODO: need the platform API to get the allowed origin
                      data=json.dumps(payloads), headers=headers)
    return json.loads(r.text)

