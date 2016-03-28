# coding=utf-8
from __future__ import absolute_import

from flask import g, current_app
from utils.helpers import now


def get_access_token(code=None):
    user = g.curr_user
    access_token = user["access_token"]
    refresh_token = user["refresh_token"]
    expires_in = g.curr_user["expires_in"]
    if not code and access_token and refresh_token and expires_in:
        if now() < expires_in:
            return access_token
        else:
            try:
                resp = current_app.sup_oauth.refresh_access_token(
                    refresh_token)
                assert "access_token" in resp
            except Exception as e:
                raise RequestAccessTokenFailed(str(e))
            _save_token(user, resp)
            return resp["access_token"]
    try:
        resp = current_app.sup_oauth.get_access_token(code)
        assert "access_token" in resp
    except Exception as e:
        raise RequestAccessTokenFailed(str(e))
    _save_token(user, resp)
    return resp["access_token"]


def _save_token(user, resp):
    user["access_token"] = resp["access_token"]
    user["refresh_token"] = resp["refresh_token"]
    user["expires_in"] = now() + resp["expires_in"]
    user.save()
