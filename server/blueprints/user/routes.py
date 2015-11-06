# coding=utf-8
from __future__ import absolute_import

from .controllers import *

urlpatterns = [
    ("/ext_token/<open_id>", get_ext_token, "GET"),
    ("/sup_auth", get_sup_token, "POST"),
    ("/token_check", token_check, "POST"),
    ("/alias", get_alias, "GET"),
    ("/alias", set_alias, "POST")
]
