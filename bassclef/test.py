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

"""test.py - bassclef installation tests"""

import os
import sys
import subprocess
import textwrap

import bassclef.util
from bassclef.util import printline, which

# Get the python executable
PYTHON3 = os.path.split(sys.executable)[1]


def error(msg, e=None):
    """Error handler."""
    if hasattr(e, 'returncode'):
        bassclef.util.error(textwrap.dedent(msg), e.returncode)
    else:
        bassclef.util.error(textwrap.dedent(msg))


def check_python():
    """Checks python."""

    # Test python from the shell
    try:
        subprocess.check_output([PYTHON3, '--version'])
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        msg = """
        Call to 'python' failed.  Please submit an Issue to 
        https://github.com/tomduck/bassclef."""
        error(msg, e)
    return PYTHON3


def check_make():
    """Checks make."""

    if which('make') is None:
        error("Cannot find 'make'.")

    # Test make from the shell
    try:
        subprocess.check_output(['make', '--version'])
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        msg = """
        Call to 'make' failed.  Please submit an Issue to 
        https://github.com/tomduck/bassclef."""
        error(msg, e)

    return 'make'


def check_pandoc(args):
    """Checks pandoc."""

    if which('pandoc') is None:
        errormsg = """
        Cannot find 'pandoc'. To download pandoc, see:
        https://github.com/jgm/pandoc/releases/latest"""
        error(textwrap.dedent(errormsg))

    try:
        subprocess.check_output(['pandoc', '--version'])
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        msg = """
        Call to 'pandoc' failed.  Please submit an Issue to
        https://github.com/tomduck/bassclef."""
        error(msg, e)

    return pandoc


def check_convert(args):
    """Checks ImageMagick convert."""

    errormsg = """
    Cannot find ImageMagick 'convert'. To download ImageMagick, see:
    https://www.imagemagick.org/script/binary-releases.php"""

    if which('convert') is None:
        error(errormsg)

    try:
        output = subprocess.check_output(['convert', '--version'])
        output = output.decode(encoding='UTF-8')
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        msg = """
        Call to 'convert' failed.  Please submit an Issue to
        https://github.com/tomduck/bassclef."""
        error(msg, e)

    if not 'ImageMagick' in output:  # It must be a different 'convert'
        error(errormsg)

    return convert


#----------------------------------------------------------------------------
# test()

def test(args):
    """Runs the tests."""

    printline('Checking python... ')
    check_python()
    printline('OK.\n')

    printline('Checking make... ')
    check_make()
    printline('OK.\n')

    printline('Checking pandoc... ')
    check_pandoc(args)
    printline('OK.\n')

    printline('Checking convert... ')
    check_convert(args)
    printline('OK.\n')

