# coding=utf-8
from __future__ import absolute_import

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import requests
import json
from flask import current_app


class SupAuth(object):
    def __init__(self, app_key, app_secret, grant_type, secret_key, redirect_uri, expired_in=3600):
        self._s = Serializer(secret_key, expired_in)
        self.app_key = app_key
        self.app_secret = app_secret
        self.grant_type = grant_type
        self.redirect_uri = redirect_uri

    def generate_ext_token(self, open_id):
        return self._s.dumps({'open_id': open_id}).decode('utf-8')

    def parse_ext_token(self, token):
        try:
            data = self._s.loads(token)
        except Exception:
            return None
        return data['open_id']

    def get_access_token(self, code):
        payloads = {
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'code': code,
            'grant_type': self.grant_type,
            'redirect_uri': self.redirect_uri
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(current_app.config.get('TOKEN_URL'), data=json.dumps(payloads), headers=headers)
        return json.loads(r.text)

    def refresh_access_token(self, refresh_token):
        payloads = {
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'refresh_token': refresh_token,
            'response_type': "refresh_token",
        }
        headers = {'content-type': 'application/json'}

        r = requests.post(current_app.config.get('TOKEN_URL'), data=json.dumps(payloads), headers=headers)
        return json.loads(r.text)
    
    def check_access_token(self, access_token):
        payloads = {
            'app_key': self.app_key,
            'app_secret': self.app_secret,
            'access_token': access_token,
            'response_type': "access_token",
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(current_app.config.get('TOKEN_URL'), data=json.dumps(payloads), headers=headers)
        return json.loads(r.text)