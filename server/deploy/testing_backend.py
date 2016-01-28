#coding=utf-8
from __future__ import absolute_import
import multiprocessing

bind = "127.0.0.1:5001"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = "/data/deployment_data/logs/comment_backend.access.log"
errorlog = "/data/deployment_data/logs/comment_backend.error.log"
pidfile = "/data/deployment_data/logs/comment_backend.pid"
raw_env = "SUPMICE_CONFIG_NAME=testing"