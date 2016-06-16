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

"""bcms.py - Bassclef CMS"""

import argparse

from bassclef.test import test
from bassclef.init import init
from bassclef.make import make
from bassclef.preprocess import preprocess
from bassclef.postprocess import postprocess
from bassclef.compose import compose
from bassclef.feed import feed
from bassclef.serve import serve
from bassclef.util import printline


def main():
    """Main program."""

    # Create a top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # 'test'
    subparser = subparsers.add_parser('test')
    subparser.set_defaults(func=test)

    # 'init'
    subparser = subparsers.add_parser('init')
    subparser.add_argument('--force', '-f', action='store_true')
    subparser.add_argument('--extras', '-e', action='store_true')
    subparser.set_defaults(func=init)

    # 'make'
    subparser = subparsers.add_parser('make')
    subparser.add_argument('target', nargs='*', default='')
    subparser.set_defaults(func=make)

    # 'preprocess'
    subparser = subparsers.add_parser('preprocess')
    subparser.add_argument('path')
    subparser.set_defaults(func=preprocess)

    # 'postprocess'
    subparser = subparsers.add_parser('postprocess')
    subparser.set_defaults(func=postprocess)

    # 'compose'
    subparser = subparsers.add_parser('compose')
    subparser.add_argument('path')
    subparser.set_defaults(func=compose)

    # 'feed'
    subparser = subparsers.add_parser('feed')
    subparser.add_argument('path')
    subparser.set_defaults(func=feed)

    # 'serve'
    subparser = subparsers.add_parser('serve')
    subparser.set_defaults(func=serve)

    # Parse the args and call whatever function was selected
    args, other_args = parser.parse_known_args()
    if hasattr(args, 'func'):
        if args.func.__name__ == 'make':
            args.func(args, other_args)
        elif other_args:
            printline('Unknown options: ' + ' '.join(other_args) + '\n')
        else:
            args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
