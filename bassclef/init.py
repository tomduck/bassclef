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
import glob

from pkg_resources import resource_string  # pylint: disable=no-name-in-module


def writefile(src, dest, hide=False, force=False):
    """Reads path from package_data and writes it to disk.

    src - the source file relative to bassclef/
    dest - the destination
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
    with open(dest, 'wb') as f:
        f.write(content)


def init(args):
    """Initializes a bassclef site."""

    write = functools.partial(writefile, force=args.force)

    write('init-data/Makefile', 'Makefile', hide=True)
    write('init-data/config.ini', 'config.ini')

    write('init-data/markdown/module.mk', 'markdown/module.mk', hide=True)
    write('init-data/images/module.mk', 'images/module.mk', hide=True)
    write('init-data/css/module.mk', 'css/module.mk', hide=True)
    write('init-data/fonts/module.mk', 'fonts/module.mk', hide=True)
    write('init-data/javascript/module.mk', 'javascript/module.mk', hide=True)

    if args.extras:
        write('init-data/css/bassclef.css', 'css/bassclef.css')

        write('init-data/images/powered-by-bassclef.png',
              'images/powered-by-bassclef.png')

        write('init-data/templates/default.html5', 'templates/default.html5')
        write('init-data/templates/entry.html5', 'templates/entry.html5')

        write('submodules/skeleton/css/skeleton.css',
              'css/skeleton/skeleton.css')
        write('submodules/skeleton/css/normalize.css',
              'css/skeleton/normalize.css')

        write('submodules/open-sans/open-sans.css',
              'css/open-sans/open-sans.css')
        fonts = glob.glob('submodules/open-sans/fonts/*/*')
        for font in fonts:
            write(font, font.replace('submodules/open-sans/', ''))
