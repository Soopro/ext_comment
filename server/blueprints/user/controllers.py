# coding=utf-8
from __future__ import absolute_import

from flask import current_app, request, g
from utils.base_utils import output_json
from utils.request import parse_json, parse_args
from errors.general_errors import AuthenticationFailed, NotFound, PermissionDenied
from errors.validation_errors import ObjectIdStructure, UrlStructure
from errors.bp_users_errors import (SooproAccessDeniedError,
                                    SooproRequestAccessTokenError,
                                    SooproAPIError)
import uuid


@output_json
def get_ext_token(open_id):
    ObjectIdStructure(open_id)
    
    user = current_app.mongodb_conn.User.find_one_by_open_id(open_id)
    
    if not user:
        user = current_app.mongodb_conn.User()

    app_key = current_app.config.get('APP_KEY')
    
    state = unicode(uuid.uuid4())

    user['open_id'] = open_id
    user['random_string'] = state
    user.save()
    
    remote_oauth_url = current_app.config.get('REMOTE_OAUTH_URL')
    redirect_uri = current_app.config.get('REDIRECT_URI')

    return {
        'state': state,
        'auth_uri': remote_oauth_url,
        'app_key': app_key,
        'response_type': 'code',
        'redirect_uri': redirect_uri
    }


@output_json
def get_sup_token(): #code to here
    data = request.get_json()
    open_id = data.get('open_id')

    user = current_app.mongodb_conn.User.find_one_by_open_id(open_id)

    if not user:
        raise NotFound('user not found')
 
    if user.get('random_string') != data.get('state'):
        raise PermissionDenied('state is not equal')

    try:
        resp = current_app.sup_auth.get_access_token(data['code'])
    except Exception, e:
        print e
        raise SooproRequestAccessTokenError
        
    if not 'access_token' in resp:
        print resp
        raise SooproAPIError('Soopro OAuth2 get token error: '+str(data))

    user['access_token'] = resp['access_token']
    user['refresh_token'] = resp['refresh_token']
    user['expires_in'] = resp['expires_in']

    ext_token = current_app.sup_auth.generate_ext_token(open_id)
    user['ext_token'] = ext_token

    user.save()

    return {
        'ext_token': ext_token
    }
    
    
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

