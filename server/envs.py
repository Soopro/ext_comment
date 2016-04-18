# coding=utf-8
from __future__ import absolute_import

import os

default_config_name = "development"

CONFIG_NAME = os.getenv("SUP_EXT_COMMENT_CONFIG_NAME", None)
