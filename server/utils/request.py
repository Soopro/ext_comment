# coding=utf-8
from __future__ import absolute_import

from flask import request, current_app, g
from errors.general_errors import ErrInvalidRequestBody, \
    ErrRequestBodyNotExists
from errors.validation_errors import ValidationParameterRequired
from errors.general_errors import AuthenticationFailed


def parse_json():
    source = request.json
    if source is None:
        raise ErrRequestBodyNotExists
    if not isinstance(source, dict):
        raise ErrInvalidRequestBody
    return ParsedBody(source)


def parse_args():
    new = dict()
    args = request.args
    for arg in args:
        new[arg] = args.get(arg)
    return new


def make_query(args):
    query = ""
    for arg in args:
        s = "{}={}".format(arg,
                           args.get(arg)) if query == "" else "&{}={}".format(
            arg, args.get(arg))
        query = "{}{}".format(query, s)
    return query


class ParsedBody(dict):
    def get_params(self, *args):
        if len(args) == 0:
            return None
        if len(args) == 1:
            return self._get_one(args[0])
        return [self._get_one(key) for key in args]

    def _get_one(self, key):
        return self.get(key)

    def get_required_params(self, *args):
        if len(args) == 0:
            return None
        if len(args) == 1:
            return self._get_required_one(args[0])
        return [self._get_required_one(key) for key in args]

    def _get_required_one(self, key):
        try:
            v = self.__getitem__(key)
        except KeyError:
            raise ValidationParameterRequired(key)
        return v


def verify_token(debug=False):
    if debug:
        g.current_user = current_app.mongodb_conn.User.find_one()
        return

    ext_token = request.headers.get('Authorization')
    if ext_token is None:
        raise AuthenticationFailed(
            'Authorization(token) Required, Authorization header was missing')

    open_id = current_app.sup_auth.parse_ext_token(ext_token)

    if not open_id:
        raise AuthenticationFailed('invalid token')

    current_user = current_app.mongodb_conn.User.find_one_by_open_id(open_id)
    if current_user is None:
        raise AuthenticationFailed("User Not Exist")
    print "openid", open_id
    g.current_user = current_user
    return
