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
import threading

from bassclef.util import printline

PORT = 8000

def serve(args):
    """Runs a test server."""

    os.chdir('www')

    # Set up the server
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(('', PORT), Handler)
    httpd.allow_reuse_address = True
    
    printline('Serving at http://127.0.0.1:%d/ (^C to exit)...\n'%PORT)

    # Catch ^C and exit gracefully
    def signal_handler(signal, frame):
        printline('\n')
        httpd.shutdown()
        httpd.server_close()
    signal.signal(signal.SIGINT, signal_handler)

    thread = threading.Thread(target=httpd.serve_forever)
    thread.start()

    sys.exit(0)
