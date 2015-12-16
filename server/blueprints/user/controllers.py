# coding=utf-8
from __future__ import absolute_import

from flask import current_app, request, g
from utils.base_utils import output_json
from utils.request import parse_json, parse_args
from errors.general_errors import (AuthenticationFailed, NotFound,
                                   PermissionDenied)
from errors.validation_errors import ObjectIdStructure, UrlStructure
from errors.bp_users_errors import (SooproAccessDeniedError,
                                    SooproRequestAccessTokenError,
                                    SooproRefreshAccessTokenError,
                                    SooproAPIError)
import uuid
from utils.base_utils import now


@output_json
def get_new_ext_token(open_id):
    ObjectIdStructure(open_id)

    User = current_app.mongodb_conn.User

    user = User.find_one_by_open_id(open_id)

    if not user:
        user = User()
        user['open_id'] = open_id
        user['status'] = User.STATUS_INACTIVATED

    app_key = current_app.config.get('APP_KEY')
    state = unicode(uuid.uuid4())

    user['random_string'] = state
    user.save()

    remote_oauth_url = current_app.config.get('REMOTE_OAUTH_URL')
    redirect_uri = current_app.config.get('REDIRECT_URI')

    print user
    return {
        'state': state,
        'auth_uri': remote_oauth_url,
        'app_key': app_key,
        'response_type': 'code',
        'redirect_uri': redirect_uri
    }


@output_json
def get_sup_token():  # code to here
    data = request.get_json()

    open_id = data.get('open_id')

    user = current_app.mongodb_conn.User.find_one_by_open_id(open_id)

    if not user:
        raise NotFound('user not found')

    if user.get('random_string') != data.get('state'):
        raise PermissionDenied('state is not equal')


    if not current_app.config.get('DEBUG'):
        resp = remote_user_auth(user)
    else:
        resp = {
            'access_token': u'debug_access_token',
            'refresh_token': u'debug_refresh_token',
            'expires_in': now()+(3600*24),
            'display_name': u'DEBUGER'
        }

    user['access_token'] = resp['access_token']
    user['refresh_token'] = resp['refresh_token']
    user['expires_in'] = resp['expires_in']
    user['display_name'] = u''  # TODO display name

    user['ext_token'] = current_app.sup_auth.generate_ext_token(open_id)
    user.save()
    
    CommentExtension = current_app.mongodb_conn.CommentExtension
    comment_extention = CommentExtension.find_one_by_open_id(open_id)
    if not comment_extention:
        comment_extention = CommentExtension()
        comment_extention.user_id = user["_id"]
        comment_extention.save()
    return {
        "id": user['_id'],
        "display_name": user['display_name'],
        "alias": user['alias'],
        "status": user['status'],
        "ext_token": user['ext_token']
    }


def remote_user_auth(user):
    resp = None
    if user['access_token'] and user['expires_in'] > now():
        access_token = user['access_token']
        try:
            resp = current_app.sup_auth.check_access_token(access_token)
        except Exception, e:
            raise SooproRequestAccessTokenError
    else:
        refresh_token = user['refresh_token']
        if not refresh_token:
            try:
                resp = current_app.sup_auth.get_access_token(data['code'])
            except Exception, e:
                raise SooproRequestAccessTokenError
        else:
            try:
                resp = current_app.sup_auth.refresh_access_token(refresh_token)
            except Exception, e:
                raise SooproRefreshAccessTokenError

        if resp.get('errcode') or \
        not isinstance(resp.get('access_token'), basestring):
            current_app.logger.warn(str(resp))
            resp = None

    if not resp:
        raise SooproAPIError('Soopro OAuth2 Token error: ' + str(data))

    return resp


@output_json
def get_alias():
    user = g.current_user
    return {
        "open_id": unicode(user.open_id),
        "alias": user.alias
    }


@output_json
def set_alias():
    user = g.current_user
    data = request.get_json()
    user.alias = data.get("alias")
    user.save()
    return {
        "open_id": unicode(user.open_id),
        "alias": user.alias
    }


@output_json
def token_check():
    ext_token = request.get_json().get('ext_token')
    open_id = current_app.sup_auth.parse_ext_token(ext_token)
    user = current_app.mongodb_conn.User.find_one_by_open_id(open_id)
    if user:
        return {'status': 'OK'}
    return {'error': 'user not found'}
