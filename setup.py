#! /usr/bin/env python3

"""setup.py - install script for bassclef."""

import sys
import os, os.path
import shutil
import pip
import subprocess
import textwrap
import urllib
import zipfile

VERSION = '0.1'

SUBMODULES = ['font-awesome', 'html5shiv', 'open-sans', 'skeleton']

URLS = ['https://github.com/' + path for path in
        ['tomduck/bassclef-font-awesome/archive/master.zip',
         'aFarkas/html5shiv/archive/master.zip',
         'tomduck/bassclef-open-sans/archive/gh-pages.zip'
         'dhg/Skeleton/archive/master.zip']]


#----------------------------------------------------------------------------

def check_for_binaries():
    """Checks that binary dependencies are installed."""

    # Check that python >= 3 is being used by this script
    if sys.version.split()[0] < '3':
        msg = """

        Python %s detected.  This script must be run using python 3:

        $ python3 setup.py --user install

        Please ensure that 'python3' is installed and available from the
        command line.

        To download python3, see:

            https://www.python.org/downloads/

        """ % (sys.version.split()[0],)
        print(textwrap.dedent(msg))
        sys.exit(1)


    # Check for python3's availability on the command line
    if shutil.which('python3') is None:
        msg = """

        Cannot find 'python3'.  Please ensure that 'python3' is available from
        the command line.

        To download python3, see:

            https://www.python.org/downloads/

        """
        print(textwrap.dedent(msg))
        sys.exit(2)


    # Check for make
    if shutil.which('make') is None:
        msg = """

        Cannot find 'make'.  Please ensure that 'make' is available from
        the command line.

        Please submit an Issue to the bassclef developers:

            https://github.com/tomduck/bassclef

        """
        print(textwrap.dedent(msg))
        sys.exit(3)


    # Check for pandoc
    if shutil.which('pandoc') is None:
        msg = """

        Cannot find 'pandoc'.  Please ensure that 'pandoc' is available from
        the command line.

        To download pandoc, see:

            https://github.com/jgm/pandoc/releases/latest

        """
        print(textwrap.dedent(msg))
        sys.exit(4)


    # Check for ImageMagick convert
    if shutil.which('convert') is None:
        msg = """

        Cannot find ImageMagick 'convert'.  Please ensure that 'convert' is
        available from the command line.

        To download ImageMagick, see:

            https://www.imagemagick.org/script/binary-releases.php

        """
        print(textwrap.dedent(msg))
        sys.exit(5)

#----------------------------------------------------------------------------

def install_submodules():
    """Installs bassclef's submodules."""

    import git # Cannot import until it is installed

    # Is this a git repository?
    try:
        repo = git.Repo('.')
    except git.exc.InvalidGitRepositoryError:
        repo = None

    # Install the submodules
    if repo:   # Use git
        #repo.git.submodule('update', '--init')
        repo.submodule_update(init=True, recursive=False)
    else:  # Do it manually

        def prog():
            """Progress meter."""
            n = 0
            while True:
                if n%10 == 0:
                    print('.', end='')
                    sys.stdout.flush()
                yield
                n += 1

        os.chdir('submodules')

        for submodule, url in zip(SUBMODULES, URLS):
            if not os.listdir(submodule):

                os.rmdir(submodule)

                print('Downloading', end='')
                urllib.request.urlretrieve(url, 'download.zip', prog().next)
                print('Done. \n')

                z = zipfile.ZipFile('download.zip', 'r')
                dirname = os.path.commonprefix(z.namelist())
                z.extractall()
                z.close()

                os.rename(dirname, submodule)

        os.chdir('..')

#----------------------------------------------------------------------------

def test():
    """Tests the install."""

    if subprocess.call('make') != 0:

        msg = """

        'make' failed (error code %d).  Please submit an Issue to the bassclef
        developers:

            https://github.com/tomduck/bassclef

        """
        print(textwrap.dedent(msg))
        sys.exit(7)

#----------------------------------------------------------------------------

def finish():
    """Finishes up."""

    msg = """

    Bassclef installed successfully and all test have succeeded.

    """
    print(textwrap.dedent(msg))

#----------------------------------------------------------------------------

def main():
    """Main program."""

    check_for_binaries()
    pip.main('install pyyaml --user'.split())
    pip.main('install gitpython --user'.split())
    install_submodules()
    test()
    finish()

if __name__ == '__main__':
    main()
