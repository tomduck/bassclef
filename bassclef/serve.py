#! /usr/bin/env python3

# Copyright 2015, 2016 Thomas J. Duck <tomduck@tomduck.ca>

# This file is part of bassclef.
#
#  Bassclef is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License verson 3 as
#  published by the Free Software Foundation.
#
#  Bassclef is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with bassclef.  If not, see <http://www.gnu.org/licenses/>.

"""serve.py - test Web server"""

import os
import http.server
import socketserver
import signal
import sys

from bassclef.util import printline

PORT = 8000


# Catch ^C and exit gracefully
def signal_handler(signal, frame):
    printline('\n')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def serve(args):
    os.chdir('www')
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(('', PORT), Handler)
    printline('Serving at http://127.0.0.1:%d/ (^C to exit)...\n'%PORT)
    httpd.serve_forever()
