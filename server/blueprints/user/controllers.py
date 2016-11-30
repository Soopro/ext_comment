# coding=utf-8
from __future__ import absolute_import

from flask import current_app, g

from utils.helpers import now, pre_process_scope
from utils.api_utils import output_json
from utils.request import get_param

from apiresps.validations import Struct

from .errors import (RequestAccessTokenFailed,
                     LogoutAccessTokenFailed,
                     UserTokenFailed,
                     UserProfileFailed,
                     UserStateInvalid)


@output_json
def get_oauth_access_code(open_id):
    Struct.Id(open_id)

    state = current_app.sup_oauth.make_random_string(open_id)

    ext_key = current_app.config.get('EXT_KEY')
    redirect_uri = current_app.config.get('OAUTH_REDIRECT_URI')

    return {
        'state': state,
        'ext_key': ext_key,
        'response_type': 'code',
        'redirect_uri': redirect_uri
    }


@output_json
def get_oauth_access_token(open_id):
    Struct.Id(open_id)

    state = get_param('state', Struct.Sid, True)
    code = get_param('code', Struct.Sid, True)

    if not current_app.sup_oauth.match_random_string(state, open_id):
        raise UserStateInvalid

    ExtUser = current_app.mongodb.ExtUser

    user = ExtUser.find_one_by_open_id(open_id)

    if not user:
        user = ExtUser()
        user['open_id'] = open_id

    try:
        resp = current_app.sup_oauth.get_access_token(code)
        print resp
        assert 'access_token' in resp
    except Exception as e:
        raise RequestAccessTokenFailed('access')

    try:
        profile = current_app.sup_oauth.get_profile(resp['access_token'])
    except current_app.sup_oauth.OAuthInvalidAccessToken as e:
        raise RequestAccessTokenFailed('profile')
    except Exception as e:
        raise UserProfileFailed(str(e))

    try:
        ext_token = current_app.sup_oauth.generate_ext_token(open_id)
    except Exception as e:
        raise UserTokenFailed(str(e))

    user['access_token'] = resp['access_token']
    user['refresh_token'] = resp['refresh_token']
    user['expires_at'] = resp['expires_in'] + now()
    user['token_type'] = resp['token_type']
    user['status'] = ExtUser.STATUS_ACTIVATED

    user['display_name'] = profile['display_name']
    user['title'] = profile['title']
    user['locale'] = profile['locale']
    user['description'] = profile['description']
    user['type'] = profile['type']
    user['snapshot'] = profile['snapshot']
    user['scope'] = pre_process_scope(profile['owner_alias'],
                                      profile['app_alias'])
    user.save()

    logged_user = output_user(user)
    logged_user['token'] = ext_token

    return logged_user


@output_json
def check_user(open_id):
    Struct.Id(open_id)

    user = g.curr_user

    result = True

    if not user \
            or user['open_id'] != open_id \
            or not user["refresh_token"] \
            or not user["scope"]:
        result = False

    return {
        'result': result
    }


@output_json
def logout_user(open_id):
    Struct.Id(open_id)

    user = g.curr_user

    if user:
        try:
            current_app.sup_oauth.logout(user['access_token'])
        except Exception:
            raise LogoutAccessTokenFailed

        user['access_token'] = None
        user['refresh_token'] = None
        user.save()

    return output_user(user)

# outputs


def output_user(user):
    if not user:
        user = {}
    return {
        'id': user.get('_id'),
        'app': user.get('app'),
        'owner': user.get('owner'),
        'status': user.get('status'),
        'access_token': bool(user.get('access_token')),
        'refresh_token': bool(user.get('refresh_token')),
    }
