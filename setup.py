"""setup.py - install script for bassclef"""

# Copyright 2015, 2016 Thomas J. Duck.
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import subprocess
import textwrap
import itertools
import glob

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, dist
from setuptools.command.install import install
from setuptools.command.install_scripts import install_scripts

import distutils

from bassclef.util import error

DESCRIPTION = """Bassclef CMS."""

VERSION = '0.1'

# Check the python version
if sys.version_info < (3, ):
    error('Python >= 3 required.')


setup(
    name='Bassclef CMS',
    version=VERSION,

    author='Thomas J. Duck',
    author_email='tomduck@tomduck.ca',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    license='GPL',
    keywords='bassclef cms',
    url='https://github.com/tomduck/bassclef',
    download_url='https://github.com/tomduck/bassclef/tarball/'+VERSION,

    install_requires=['pyyaml', 'pandoc-tpp'],

    packages=['bassclef'],

    entry_points={'console_scripts':['bcms = bassclef.bcms:main']},

    include_package_data = True,
    package_data = {'bassclef': ['init-data/Makefile',
                                 'init-data/config.ini',
                                 'init-data/markdown/*.*',
                                 'init-data/images/*.*',
                                 'init-data/css/*.*',
                                 'init-data/fonts/*.*',
                                 'init-data/javascript/*.*',
                                 'init-data/templates/*.*',
                                 'init-data/submodules/skeleton/css/*.*',
                                 'init-data/submodules/html5shiv/src/*.*',
                                 'init-data/submodules/open-sans/css/*.*',
                                 'init-data/submodules/open-sans/fonts/*/*.*',
                                 'init-data/submodules/font-awesome/css/*.*',
                                 'init-data/submodules/font-awesome/fonts/*.*'
                                 ]},

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python'
        ],
)
