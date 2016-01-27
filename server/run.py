# coding=utf-8
from __future__ import absolute_import

from application import create_app
import argparse

parser = argparse.ArgumentParser(
                description='Options of starting Supmice server.')

parser.add_argument('-t', '--test', 
                    dest='server_mode',
                    action='store_const',
                    const="testing",
                    help='Manually start debug as testing config.')

parser.add_argument('-p', '--production', 
                    dest='server_mode',
                    action='store_const',
                    const="production",
                    help='Manually start debug as production config.')

args, unknown = parser.parse_known_args()
    
app = create_app(args.server_mode or "development")


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5001)
