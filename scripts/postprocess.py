#! /usr/bin/env python3

# This file is part of bassclef.
#
#  bassclef is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License verson 3 as
#  published by the Free Software Foundation.
#
#  bassclef is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with bassclef.  If not, see <http://www.gnu.org/licenses/>.

"""postprocess.py - a pandoc html postprocessor.

  Usage: preprocess.py src/.../filename.md

  This script reads pandoc html from stdin, postprocesses it, and
  writes the result to stdout.
"""

import sys
import re


def postprocess():
    """Postprocesses output piped from pandoc."""

    # Get the lines
    lines = [line for line in sys.stdin]


    ## Essential fixes ##

    # Fix buggy output in old pandoc version used by Debian jessie
    old = '&lt;span class=&quot;fa fa-envelope badge&quot;&gt;&lt;/span&gt;'
    new = '<span class="fa fa-envelope badge"></span>'
    for i, line in enumerate(lines):
        lines[i] = line.replace(old, new)


    ## Functionality fixes ##

    # Link thumbnail figure images to their larger versions
    p = re.compile('(<img src="/img/thumbs/(.*)" .*? />)')
    for i, line in enumerate(lines):
        if p.search(line):
            tag, img = p.search(line).groups()
            html = '<a href="/img/%s">%s</a>' % (img, tag)
            lines[i] = line.replace(tag, html)


    ## Aesthetic fixes to html ##

    # Add some space around hr tags
    for i, line in enumerate(lines):
        lines[i] = line.replace('<hr />', '\n<hr />\n')

    # Don't separate /divs from their descriptions
    for i, line in enumerate(lines[:-1]):
        if line.startswith('</div>') and lines[i+1].strip().startswith('<!--'):
            lines[i] = lines[i][:-1] + ' ' + lines[i+1]
            lines[i+1] = None


    ## Output ##

    # Print to stdout
    lines = [line for line in lines if line != None]
    print(''.join(lines))


if __name__ == '__main__':
    postprocess()

