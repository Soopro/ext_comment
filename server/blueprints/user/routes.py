# coding=utf-8
from __future__ import absolute_import

from .controllers import *

urlpatterns = [
    ("/<open_id>", get_oauth_access_code, "GET"),
    ("/<open_id>", get_oauth_access_token, "POST"),
    ("/<open_id>", logout_user, "DELETE"),
    ("/<open_id>/check", check_user, "POST"),
]
