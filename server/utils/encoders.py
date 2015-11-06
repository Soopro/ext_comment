#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import json
from bson import ObjectId


class Encoder(json.JSONEncoder):
    """
    This is our customized JSONEncoder
    if the obj is instance of datetime, encode as isoformat
    if the obj is instance of bson.ObjectId, encode as string repr
    """
    # FMT = '%Y-%m-%d'

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        return obj