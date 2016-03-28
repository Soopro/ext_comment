# coding=utf-8
from __future__ import absolute_import

from flask import request, current_app
import os

from apiresps.errors import (InvalidRequestBody,
                             RequestMaxLimited,
                             RequestBlocked,
                             RequestBodyNotExists)
from apiresps.validations import ValidationParameterRequired


def _check_request_source(req_type):
    try:
        source = getattr(request, req_type)
    except Exception:
        raise InvalidRequestBody
    if source is None:
        raise RequestBodyNotExists
    if not isinstance(source, dict):
        raise InvalidRequestBody
    return source


def is_empty_value(value):
    return value is not False and value != 0 and not bool(value)


def get_param(key, validator=None, required=False, default=None):
    source = _check_request_source('json')
    value = source.get(key)

    if is_empty_value(value):
        if default is not None:
            value = default
        elif required:
            raise ValidationParameterRequired(key)

    if validator:
        validators = validator if isinstance(validator, list) else [validator]

        for vld in validators:
            if not hasattr(vld, '__call__'):
                continue
            vld(value, name=key, non_empty=required)

    return value


def parse_args():
    new = dict()
    args = request.args
    for arg in args:
        if arg in new:
            if not isinstance(new[arg], list):
                new[arg] = [new[arg]]
            new[arg].append(args.get(arg))
        else:
            new[arg] = args.get(arg)
    return new


def make_query(args):
    query = ""
    for arg in args:
        s = "{}={}".format(arg, args.get(arg)) if query == "" \
            else "&{}={}".format(arg, args.get(arg))

        query = "{}{}".format(query, s)
    return query


def get_remote_addr():
    ip = request.headers.get('X-Forwarded-For')
    if ip:
        ip = ip.split(',', 1)[0]
    else:
        ip = request.headers.get('X-Real-IP', request.remote_addr)
    return ip


def get_request_path(user_alias, app_alias):
    apps_prefix = current_app.config.get("APPS_PREFIX")
    app_base_path = os.path.normpath(
        os.path.join(apps_prefix, user_alias, app_alias)
    )
    return request.path.replace(app_base_path, '', 1) or '/'


def rate_limit(key, remote_addr=None, limit=600, expires_in=3600):
    rate_prefix = current_app.config['RATE_LIMIT_PREFIX']
    bad_ip_prefix = current_app.config['INVALID_REMOTE_ADDR_PREFIX']
    bad_ip_limit = current_app.config['INVALID_REMOTE_ADDR_LIMIT']
    bad_ip_expire = current_app.config['INVALID_REMOTE_ADDR_EXPIRATION']

    bad_ip_key = "{}/{}".format(bad_ip_prefix, remote_addr)
    rate_key = "{}{}/{}".format(rate_prefix, key,
                                remote_addr or get_remote_addr())

    redis = current_app.redis

    bad_ip = redis.get(bad_ip_key)
    if bad_ip > bad_ip_limit:
        raise RequestBlocked

    curr = redis.get(rate_key)
    if current_app.debug:
        print "-----------------"
        print "current key:", rate_key
        print "current rate:", curr, '/', limit
        print "timer remain:", redis.ttl(rate_key)
        print "-----------------"
    p = redis.pipeline()
    if curr and int(curr) > limit:
        p.incr(bad_ip_key)
        p.expire(bad_ip_key, bad_ip_expire)
        if bad_ip > bad_ip_limit/2:
            record_bad_remote_addr(bad_ip, rate_key)
        raise RequestMaxLimited
    if not curr:
        p.setex(rate_key, 0, expires_in)
    p.incr(rate_key)
    p.execute()


def record_bad_remote_addr(bad_addr, rate_key):
    bad_addr = current_app.mongodb_conn.\
        BadRemoteAddr.find_one_by_addr(bad_addr)
    if not bad_addr:
        bad_addr = current_app.mongodb_conn.BadRemoteAddr()
        bad_addr["requests"] = []
        bad_addr["risk"] = 0

    bad_addr["remote_addr"] = bad_addr
    bad_addr["requests"].append({
        'url': request.url,
        'referrer': request.referrer,
        'user_agent': request.user_agent.string,
        'rate_key': rate_key,
    })
    bad_addr["risk"] += 1
    bad_addr.save()
