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

# pylint: disable=no-name-in-module
from pkg_resources import resource_string, resource_listdir, resource_isdir

from bassclef.util import printline


def writefile(src, dest, hide=False, force=False):
    """Writes files from src package data to dest.

    hide - if True, prepends a dot to the filename
    force - if True, overwrites existing files
    """

    if hide:  # Prepend a dot to the filename to hide it
        head, tail = os.path.split(dest)
        dest = os.path.join(head, '.' + tail)

    # Bail out if the destination already exists
    if os.path.exists(dest) and not force:
        return

    # Read from package data
    content = resource_string('bassclef', src)

    # Create the directory structure
    try:
        if os.path.dirname(dest):
            os.makedirs(os.path.dirname(dest))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

    # Initialize the file
    printline('Writing %s\n'%dest)
    with open(dest, 'wb') as f:
        f.write(content)


def writefiles(src, dest, force=False, skip=['module.mk']):
    """Writes files from src package data dir to dest dir.
    
    force - if True, overwrites existing files
    skip - a list of filenames to skip
    """
    filenames = resource_listdir('bassclef', src)
    for filename in filenames:
        if filename not in skip:
            src_ = os.path.join(src, filename)
            dest_ = os.path.join(dest, filename)
            if resource_isdir('bassclef', src_):
                writefiles(src_, dest_, force, skip)
            else:
                if os.path.exists(dest_) and not force:
                    continue
                writefile(src_, dest_, force=force)


def init(args):
    """Initializes a bassclef site."""

    _writefile = functools.partial(writefile, force=args.force)
    _writefiles = functools.partial(writefiles, force=args.force)

    _writefile('init-data/Makefile', 'Makefile', hide=True)
    _writefile('init-data/config.ini', 'config.ini')

    _writefile('init-data/markdown/module.mk', 'markdown/module.mk', hide=True)
    _writefile('init-data/images/module.mk', 'images/module.mk', hide=True)
    _writefile('init-data/css/module.mk', 'css/module.mk', hide=True)
    _writefile('init-data/fonts/module.mk', 'fonts/module.mk', hide=True)
    _writefile('init-data/javascript/module.mk', 'javascript/module.mk',
               hide=True)

    if args.extras:
        _writefiles('init-data/markdown', 'markdown')
        _writefiles('init-data/css', 'css')
        _writefiles('init-data/images', 'images')
        _writefiles('init-data/javascript', 'javascript')
        _writefiles('init-data/templates', 'templates')
        _writefiles('init-data/submodules/html5shiv/src',
                    'javascript/html5shiv')
        _writefiles('init-data/submodules/skeleton/css', 'css/skeleton')
        _writefiles('init-data/submodules/open-sans/css', 'css/open-sans')
        _writefiles('init-data/submodules/open-sans/fonts', 'fonts/open-sans')
        _writefiles('init-data/submodules/font-awesome/css', 'css/font-awesome')
        _writefiles('init-data/submodules/font-awesome/fonts',
                    'fonts/font-awesome')
