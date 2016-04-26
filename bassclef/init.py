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

"""test.py - bassclef site initialization"""

import os
import errno
import functools

from pkg_resources import resource_string

from bassclef.util import error


def writefile(path, hide=False, force=False):
    """Reads path from package_data and writes it to disk.

    hide - if True, prepends a dot to the filename
    force - if True, overwrites existing files
    """

    # Bail out if the file already exists
    if os.path.exists(path) and not force:
        return

    # Read from package_data
    content = resource_string('bassclef', os.path.join('init-data', path))


    # Create the directory structure
    try:
        if os.path.dirname(path):
            os.makedirs(os.path.dirname(path))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

    if hide:  # Prepend a dot to the filename to hide it
        head, tail = os.path.split(path)
        path = os.path.join(head, '.' + tail)

    # Initialize the file
    with open(path, 'wb') as f:
        f.write(content)


def init(args):
    """Initializes a bassclef site."""

    write = functools.partial(writefile, force=args.force)
    
    write('Makefile', hide=True)
    write('config.ini')

    write('css/module.mk', hide=True)
    write('css/bassclef.css')
    
    write('images/module.mk', hide=True)
    write('images/bassclef-logo.png')
    write('images/powered-by-bassclef.png')

    write('markdown/module.mk', hide=True)
    write('markdown/index.md')

    write('templates/default.html5')
    write('templates/entry.html5')
