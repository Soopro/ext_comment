# coding=utf-8
from __future__ import absolute_import

from flask import request, current_app, json
import base64
import requests
from errors.general_errors import ExtensionNotFound, PermissionDenied





def get_allowed_origin(open_id):
    payloads = {
        'open_id': open_id
    }
    headers = {'content-type': 'application/json'}
    r = requests.post(current_app.config.get(''),
                    # TODO: need the platform API to get the allowed origin
                      data=json.dumps(payloads), headers=headers)
    return json.loads(r.text)

