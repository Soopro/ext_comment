from datetime import timedelta

from bson import ObjectId
from bson.errors import InvalidId
from flask import current_app, request, _request_ctx_stack, g
from werkzeug.local import LocalProxy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer,
                          JSONWebSignatureSerializer,
                          SignatureExpired,
                          BadSignature)
from errors.general_errors import (AuthenticationFailed,
                                   OAuth2PermissionDenied)
import json


current_user = LocalProxy(lambda: getattr(_request_ctx_stack.top,
                                          'current_user', None))
current_member = LocalProxy(lambda: getattr(_request_ctx_stack.top,
                                            'current_member', None))
current_application = LocalProxy(lambda: getattr(_request_ctx_stack.top,
                                                 'current_application', None))


class AuthFailed(Exception):
    pass


def get_serializer(expires_in=None):
    if expires_in is None:
        expires_in = current_app.config.get('JWT_EXPIRATION_DELTA', 0)
    if isinstance(expires_in, timedelta):
        expires_in = int(expires_in.total_seconds())
    expires_in_total = expires_in + current_app.config.get('JWT_LEEWAY', 0)
    return TimedJSONWebSignatureSerializer(
        secret_key=current_app.config.get('JWT_SECRET_KEY'),
        expires_in=expires_in_total,
        algorithm_name=current_app.config.get('JWT_ALGORITHM',"HS256")
    )


def get_refresh_serializer():
    return JSONWebSignatureSerializer(
        secret_key=current_app.config.get('JWT_SECRET_KEY'),
        algorithm_name=current_app.config.get('JWT_ALGORITHM',"HS256")
    )


def _load_token(realm=None):
    realm = realm or current_app.config['JWT_DEFAULT_REALM']
    auth = request.headers.get('Authorization', None)

    if auth is None:
        raise AuthFailed(
            'Authorization Required, Authorization header was missing'
            'WWW-Authenticate: JWT realm="%s"' % realm)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthFailed('Invalid JWT header' 'Unsupported authorization type')
    elif len(parts) == 1:
        raise AuthFailed('Invalid JWT header' 'Token missing')
    elif len(parts) > 2:
        raise AuthFailed('Invalid JWT header' 'Token contains spaces')
    return parts[1]


def load_payload(token):
    try:
        return get_serializer().loads(token)
    except SignatureExpired:
        raise AuthFailed('Invalid JWT' 'Token is expired')
    except BadSignature:
        raise AuthFailed('Invalid JWT' 'Token is undecipherable')


def get_current_user(redis_conn, mongodb_conn, expired_key_prefix, realm=None):
    if request.headers.get('AppKey'):
        user = _get_current_user_by_auth2(redis_conn, mongodb_conn, realm)
    else:    
        user = _get_current_user_by_logged(redis_conn, mongodb_conn, 
                                           expired_key_prefix, realm)
    return user


def _get_current_user_by_logged(redis_conn, mongodb_conn, 
                                expired_key_prefix, realm=None):
    token = _load_token(realm)

    if redis_conn.get(expired_key_prefix + token):
        raise AuthFailed('Invalid JWT token as the user has logged out!')

    payload = load_payload(token)
    try:
        uid = ObjectId(payload)
    except InvalidId:
        raise AuthFailed("Invalid uid")
    user = mongodb_conn.User.find_one_by_id(uid)
    return user


def _get_current_user_by_auth2(redis_conn, mongodb_conn, realm=None):    
    token = _load_token(realm)

    request_app_key = request.headers.get('AppKey', None)
    request_app_secret = request.headers.get('AppSecret', None)
    
    access_token = _load_token(realm)
    payload = load_payload(token)
    
    uid = payload["uid"]
    open_id = payload["open_id"]
    app_key = payload["app_key"]
    app_secret = payload["app_secret"]
    
    access_token_key = "access_token/{}/{}".format(app_key, open_id)

    if request_app_key != app_key or request_app_secret != app_secret \
    or not redis_conn.sismember(access_token_key, access_token):
        raise AuthFailed('Invalid Access token is expired!')

    try:
        uid = ObjectId(uid)
    except InvalidId:
        raise AuthFailed("Invalid Access uid")
    user = mongodb_conn.User.find_one_by_id(uid)
    
    # check request is allow by user, use request.method for now.
    if request.method != 'GET':
        raise OAuth2PermissionDenied
    return user


def get_current_member(redis_conn, mongodb_conn, expired_key_prefix,
                       realm=None):
    token = _load_token(realm)

    if redis_conn.get(expired_key_prefix + token):
        raise AuthFailed('Invalid JWT token as the member has logged out!')

    try:
        payload = load_payload(token)
        member_id = ObjectId(payload.get("member_id"))
    except InvalidId:
        raise AuthFailed("Invalid member id")
    except Exception:
        raise AuthFailed("Invalid token")

    member = mongodb_conn.Member.find_one({'_id': member_id})
    if member is None:
        raise AuthFailed("member not found")
    try:
        owner_id = ObjectId(payload.get("auth_point"))
    except InvalidId:
        raise AuthFailed("Invalid auth_point")

    user = mongodb_conn.User.find_one_by_id(owner_id)
    if user is None:
        raise AuthenticationFailed

    member_relate = mongodb_conn.\
                        MemberRelate.find_one_by_oid_and_mid(user["_id"],
                                                             member_id)
    if member_relate is None:
        raise AuthenticationFailed

    return member


def get_jwt_token():
    auth = request.headers.get('Authorization')
    parts = auth.split()
    return parts[1]


def generate_token(payload, expires_in=None):
    if not isinstance(payload, (dict, list)):
        payload = unicode(payload)
    return get_serializer(expires_in).dumps(payload).decode("utf-8")


def generate_refresh_token(payload):
    if not isinstance(payload, (dict, list)):
        payload = unicode(payload)
    return get_refresh_serializer().dumps(payload).decode("utf-8")


def generate_hashed_password(pwd):
    return unicode(generate_password_hash(pwd))


def check_hashed_password(hashed, password):
    return check_password_hash(str(hashed), password)
