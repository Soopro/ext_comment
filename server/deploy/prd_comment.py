# coding=utf-8
from __future__ import absolute_import

import multiprocessing

bind = "127.0.0.1:5001"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = "deploy/comment.access.log"
errorlog = "deploy/comment.error.log"
pidfile = "deploy/comment.pid"
raw_env = "SUP_EXT_COMMENT_CONFIG_NAME=production"
