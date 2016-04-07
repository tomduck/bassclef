#! /usr/bin/env python3

"""setup.py - setup script for bassclef."""

import sys
from sys import stdout
import os, os.path
import shutil
import pip
import subprocess
import textwrap
import urllib
import zipfile
import argparse

SUBMODULES = ['font-awesome', 'html5shiv', 'open-sans', 'skeleton']

URLS = ['https://github.com/' + path for path in
        ['tomduck/bassclef-font-awesome/archive/master.zip',
         'aFarkas/html5shiv/archive/master.zip',
         'tomduck/bassclef-open-sans/archive/gh-pages.zip',
         'dhg/Skeleton/archive/master.zip']]

PYTHON3 = sys.executable
if os.name == 'nt': # Cygwin specialization
    PYTHON3 = os.path.splitext(PYTHON3)[0]

# pylint: disable=invalid-name
parser = argparse.ArgumentParser(description='Sets up bassclef.')
parser.add_argument('--test', help='Tests installation by running make.',
                    action='store_true')
args = parser.parse_args(sys.argv[1:])

TEST = args.test

#----------------------------------------------------------------------------

def print_message(msg):
    """Prints a message to stdout and flushes the buffer."""
    stdout.write(msg)
    stdout.flush()

def error(msg, errno):
    """Writes an error message to stdout and exits."""
    print_message(textwrap.dedent(msg) + '\n')
    sys.exit(errno)

#----------------------------------------------------------------------------

def check_python():
    """Checks the python installation"""

    global PYTHON3  # pylint: disable=global-statement

    print_message('Checking python installation... ')

    # Check the python version
    if sys.version_info < (3, ):
        msg = """

        Python < 3 detected.  Please upgrade and/or call this script
        using Python 3.
        
        """
        error(msg, 1)

    # Backport which() if it is missing (python < 3.3)
    if not hasattr(shutil, 'which'):
        pip.main('install whichcraft --user'.split())
        import whichcraft  # pylint: disable=import-error
        shutil.which = whichcraft.which

    # Get a simpler call for python, if possible
    def target(name):
        """Returns the path to the named executable"""
        return shutil.which(name) if os.name != 'nt' else \
          os.path.splitext(shutil.which(name))[0]
    if  target('python3') == PYTHON3:
        PYTHON3 = 'python3'
    elif target('python') == PYTHON3:
        PYTHON3 = 'python'

    # Cygwin specialization
    if os.name == 'nt':
        PYTHON3 = PYTHON3.replace('\\', '/').replace(' ', '\\ ')

    # Test that we can call python
    try:
        subprocess.check_output('python -c "print()"')
        print_message('OK.\n')

    except subprocess.CalledProcessError as e:

        msg = """

        Call to python executable failed.  Please submit an Issue:

            https://github.com/tomduck/bassclef

        """ % e.returncode
        error(msg, 2)

    print_message('OK.\n\n')

#----------------------------------------------------------------------------

def check_binaries():
    """Checks that binary dependencies are installed."""

    # Check for make
    print_message("Is make available? ")
    if shutil.which('make') is None:
        msg = """

        Cannot find 'make'.  Please ensure that 'make' is available from
        the command line.

        """
        error(msg, 3)

    print_message('Yes.\n')


    # Check for pandoc
    print_message("Is pandoc available? ")
    if shutil.which('pandoc') is None:
        msg = """

        Cannot find 'pandoc'.  Please ensure that 'pandoc' is available from
        the command line.

        To download pandoc, see:

            https://github.com/jgm/pandoc/releases/latest

        """
        error(msg, 4)

    print_message('Yes.\n')


    # Check for ImageMagick convert
    print_message("Is convert available? ")
    if shutil.which('convert') is None:
        msg = """

        Cannot find ImageMagick 'convert'.  Please ensure that 'convert' is
        available from the command line.

        To download ImageMagick, see:

            https://www.imagemagick.org/script/binary-releases.php

        """
        error(msg, 5)

    print_message('Yes.\n\n')

#----------------------------------------------------------------------------

def install_pyyaml():
    """Installs pyyaml."""
    try:
        import yaml  # pylint: disable=unused-variable
        print_message('PyYAML found.\n')
    except ImportError:
        print_message('Installing pyyaml:\n')
        pip.main('install pyyaml --user'.split())

#----------------------------------------------------------------------------

def has_submodule(name):
    """Returns True if the submodule appeaers to be installed."""
    return os.listdir(os.path.join('submodules', name))

def install_submodules():
    """Installs submodules aggregated with bassclef."""

    # Print out a message
    flag = True
    for submodule in SUBMODULES:
        if not has_submodule(submodule):
            print_message('\nInstalling submodules:\n')
            flag = False
            break
    if flag:
        print_message('Submodules found.\n')
        return

    # Is this a git repository?
    is_repo = os.path.exists('.git')

    # Install the submodules
    if is_repo:   # Assume user has git installed

        if subprocess.call('git submodule update --init'.split()) != 0:
            msg = """

            Error installing submodules with git.  Please submit an Issue:
 
            https://github.com/tomduck/bassclef

            """
            error(msg, 6)

    else:  # Download zips and unpack them into submodules/

        def prog(n=0):
            """Progress meter."""
            while True:
                if n%20 == 0:
                    print_message('.')
                yield
                n += 1
        report = prog().__next__

        for submodule, url in zip(SUBMODULES, URLS):
            if not has_submodule(submodule):

                # Set up
                print_message('Downloading/installing %s...'%submodule)
                os.chdir('submodules')

                # Download zip
                urllib.request.urlretrieve(url, 'download.zip',
                                           lambda x, y, z: report())

                # Unpack
                z = zipfile.ZipFile('download.zip', 'r')
                dirname = os.path.commonprefix(z.namelist())
                z.extractall()
                z.close()

                # Install
                os.rmdir(submodule)
                os.rename(dirname, submodule)

                # Clean up
                os.remove('download.zip')
                os.chdir('..')
                print_message(' Done.\n')

#----------------------------------------------------------------------------

def generate_makefile():
    """Generates Makefile from Makefile.in"""

    print_message('\nGenerating Makefile...')

    # Read Makefile.in
    with open('Makefile.in') as f:
        lines = f.readlines()

    # Write Makefile.  Perform replacements as necessary.
    with open('Makefile', 'w') as f:
        for line in lines:
            if line.startswith('PYTHON3 ='):
                line = 'PYTHON3 = ' + PYTHON3 + '\n'
            f.write(line)

    print_message('Done.\n')

#----------------------------------------------------------------------------

def test():
    """Tests the install."""

    print_message('\nTesting install... ')

    try:
        subprocess.check_output('make')
        print_message('OK.\n')

    except subprocess.CalledProcessError as e:

        msg = """

        'make' failed (error code %d).  Please submit an Issue:

            https://github.com/tomduck/bassclef

        """ % e.returncode
        error(msg, 7)

#----------------------------------------------------------------------------

def finish():
    """Finishes up."""
    print_message('\nBassclef setup complete.\n\n')

#----------------------------------------------------------------------------

def main():
    """Main program."""

    print_message('\n')

    check_python()
    check_binaries()
    install_pyyaml()
    install_submodules()
    generate_makefile()
    if TEST:
        test()
    finish()

if __name__ == '__main__':
    main()
