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

import subprocess
import textwrap

import bassclef.util
from bassclef.util import write, which


def error(msg, e=None):
    """Error handler."""
    if hasattr(e, 'returncode'):
        bassclef.util.error(textwrap.dedent(msg), e.returncode)
    else:
        bassclef.util.error(textwrap.dedent(msg))


def check_python():
    """Checks python."""

    if which('python3') is None:
        error("Cannot find 'python3'.")

    # Test python from the shell
    try:
        subprocess.check_output(['python3', '--version'])
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        msg = """
        Call to 'python3' failed.  Please submit an Issue to 
        https://github.com/tomduck/bassclef."""
        error(msg, e)


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


def check_pandoc():
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


def check_convert():
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


#----------------------------------------------------------------------------
# test()

def test():
    """Runs the tests."""

    write('Checking python... ')
    check_python()
    write('OK.\n')

    write('Checking make... ')
    check_make()
    write('OK.\n')

    write('Checking pandoc... ')
    check_pandoc()
    write('OK.\n')

    write('Checking convert... ')
    check_convert()
    write('OK.\n')

