#! /usr/bin/env python3

# Copyright 2015, 2016 Thomas J. Duck <tomduck@tomduck.ca>

# This file is part of bassclef-scripts.
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

"""make.py - GNU make wrapper"""

import os.path
import subprocess
import sys

from bassclef.util import error


def make(args):
    """Builds the site via a call to GNU make."""

    # Find the Makefile
    makefile = 'Makefile' if os.path.exists('Makefile') else '.Makefile'
    if not os.path.exists(makefile):
        error('Makefile not found.')

    # Assemble the call
    command = ['make', '-f', makefile]
    if argsrebuild:
        command.append('-B')
    if args.target:
        command.append(target)

    # Make the call
    sys.exit(subprocess.call(command))
