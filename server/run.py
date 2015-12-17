# coding=utf-8
from __future__ import absolute_import

from application import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5001)
