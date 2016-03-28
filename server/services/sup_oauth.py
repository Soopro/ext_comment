# coding=utf-8
from __future__ import absolute_import

from itsdangerous import (TimedJSONWebSignatureSerializer as TimedSerializer,
                          JSONWebSignatureSerializer as Serializer)
import requests
import json


class SupOAuth(object):
    AUTH_HEADER_KEY = 'Authorization'
    AUTH_HEADER_PREFIX = 'Bearer'

    RANDOM_STRING_EXPIRES_IN = 60 * 10

    DEFAULT_EXT_EXPIRES_IN = 3600 * 24 * 1 - 1
    DEFAULT_HEADERS = {'content-type': 'application/json'}

    def __init__(self, ext_key, ext_secret, secret_key, expires_in,
                 api_uri, token_uri, redirect_uri):

        expires_in = int(expires_in.total_seconds()) or \
            self.DEFAULT_EXT_EXPIRES_IN
        self._s = TimedSerializer(
            secret_key=secret_key,
            expires_in=expires_in
        )
        self._r = TimedSerializer(
            secret_key=secret_key,
            expires_in=self.RANDOM_STRING_EXPIRES_IN
        )
        self._f = Serializer(
            secret_key=secret_key
        )
        self.ext_key = ext_key
        self.ext_secret = ext_secret
        self.api_uri = api_uri
        self.token_uri = token_uri
        self.redirect_uri = redirect_uri

    def generate_ext_token(self, open_id):
        try:
            open_id = unicode(open_id)
            token = self._s.dumps(open_id).decode('utf-8')
        except Exception as e:
            raise self.OAuthInvalidExtToken(str(e))
        return token

    def encrypt(self, code):
        try:
            code = unicode(code)
            code = self._f.dumps(code).decode('utf-8')
        except Exception as e:
            raise self.OAuthEncryptionFailed(str(e))
        return code

    def decrypt(self, code):
        try:
            code = self._f.loads(code)
        except Exception as e:
            raise self.OAuthDecryptionFailed(str(e))
        return code

    def load_ext_token(self, headers):
        auth = headers.get(self.AUTH_HEADER_KEY)
        if not auth:
            return None
        parts = auth.split()

        if parts[0].lower() != self.AUTH_HEADER_PREFIX.lower():
            return None

        try:
            token = parts[1]
            open_id = self._s.loads(token)
        except Exception:
            return None

        return open_id

    def make_random_string(self, open_id):
        try:
            open_id = unicode(open_id)
            random_string = self._r.dumps(open_id).decode('utf-8')
        except Exception as e:
            raise self.OAuthInvalidRandomString(str(e))
        return random_string

    def match_random_string(self, random_string, target_string):
        try:
            payload = self._r.loads(random_string)
        except Exception:
            payload = None
        return payload == target_string

    def get_access_token(self, code):
        payloads = {
            'ext_key': self.ext_key,
            'ext_secret': self.ext_secret,
            'code': code,
            'grant_type': 'code',
            'redirect_uri': self.redirect_uri
        }
        headers = self.DEFAULT_HEADERS
        try:
            r = requests.post(self.token_uri,
                              data=json.dumps(payloads),
                              headers=headers)
            result = r.json()
            assert isinstance(result, dict)
        except Exception:
            raise self.OAuthInvalidAccessToken

        result['access_token'] = self.encrypt(result['access_token'])
        result['refresh_token'] = self.encrypt(result['refresh_token'])

        return result

    def refresh_access_token(self, refresh_token):
        payloads = {
            'ext_key': self.ext_key,
            'ext_secret': self.ext_secret,
            'refresh_token': self.decrypt(refresh_token),
            'grant_type': "refresh_token",
        }

        headers = self.DEFAULT_HEADERS
        try:
            r = requests.post(self.token_uri,
                              data=payloads,
                              headers=headers)
            result = r.json()
            assert isinstance(result, dict)
        except:
            raise self.OAuthInvalidRefreshToken

        result['access_token'] = self.encrypt(result['access_token'])
        result['refresh_token'] = self.encrypt(result['refresh_token'])

        return result

    def request(self, method, url, access_token, **kwargs):
        headers = self.DEFAULT_HEADERS
        headers.update({
            self.AUTH_HEADER_KEY: '{} {}'.format(self.AUTH_HEADER_PREFIX,
                                                 self.decrypt(access_token))
        })

        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers'].update(headers)

        try:
            r = requests.request(method, url, **kwargs)
            result = r.json()
            assert isinstance(result, dict) or isinstance(result, list)
            assert r.status_code < 400
        except Exception as e:
            if r.status_code == 401:
                raise self.OAuthInvalidAccessToken
            elif r.status_code >= 400:
                err_msg = json.dumps(r.json())
            else:
                err_msg = str(e)
            raise self.OAuthInvalidRequest(err_msg)

        return result

    def get_profile(self, access_token):
        try:
            url = '{}/oauth/profile'.format(self.api_uri)
        except Exception as e:
            raise self.OAuthInvalidParams(str(e))
        return self.request('GET', url, access_token)

    def get_member(self, member_open_id, access_token):
        try:
            url = '{}/crm/oauth/member/{}'.format(self.api_uri,
                                                  member_open_id)
        except Exception as e:
            raise self.OAuthInvalidParams(str(e))
        return self.request('GET', url, access_token)

    def get_members(self, access_token, role='', offset=0):
        try:
            url = '{}/crm/oauth/member?role={}&offset={}'.format(self.api_uri,
                                                                 role,
                                                                 offset)
        except Exception as e:
            raise self.OAuthInvalidParams(str(e))
        return self.request('GET', url, access_token)

    def get_roles(self, access_token):
        try:
            url = '{}/crm/oauth/role'.format(self.api_uri)
        except Exception as e:
            raise self.OAuthInvalidParams(str(e))
        return self.request('GET', url, access_token)

    def logout(self, access_token):
        url = '{}/oauth/access_logout'.format(self.api_uri)
        return self.request('DELETE', url, access_token)

    # exceptions

    class OAuthException(Exception):
        status_message = 'oauth_error'

        def __init__(self, message=None):
            self.affix_message = message

        def __str__(self):
            return '{}:{}'.format(self.status_message, self.affix_message)

    class OAuthInvalidAccessToken(OAuthException):
        status_message = 'OAUTH_INVALID_ACCESS_TOKEN'

    class OAuthInvalidRefreshToken(OAuthException):
        status_message = 'OAUTH_INVALID_REFRESH_TOKEN'

    class OAuthInvalidExtToken(OAuthException):
        status_message = 'OAUTH_INVALID_EXT_TOKEN'

    class OAuthInvalidRandomString(OAuthException):
        status_message = 'OAUTH_INVALID_RANDOM_STRING'

    class OAuthInvalidRequest(OAuthException):
        status_message = 'OAUTH_INVALID_REQUEST'

    class OAuthInvalidParams(OAuthException):
        status_message = 'OAUTH_INVALID_PARAMS'

    class OAuthDecryptionFailed(OAuthException):
        status_message = 'OAUTH_DECRYPTION_FAILED'

    class OAuthEncryptionFailed(OAuthException):
        status_message = 'OAUTH_ENCRYPTION_FAILED'
