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

"""preprocess.py - a pandoc markdown preprocessor.

  Usage: preprocess.py markdown/.../filename.md

  This script reads in a pandoc markdown file, preprocesses it, and writes
  the result to stdout.
"""

import sys

from util import getmeta, printmeta, getcontent, printcontent


def insert_figure(lines, image, caption):
    """Inserts a figure into the markdown lines."""

    # Look for the image line
    n = None
    flag = False  # Flag when we have found it
    for i, line in enumerate(lines):
        if flag:
            n = i
            break
        if line == '<!-- image -->':
            n = i
            continue

    # Find the end of the first paragraph
    if n is None:
        flag = False  # Flag when we have found it
        for i, line in enumerate(lines):
            if flag:
                n = i
                break
            if line:
                flag = True
                continue

    # Insert the lines for the figure
    n = n if n is not None else len(lines)
    lines.insert(n, '\n![%s](%s)\n' % (caption, image))
    lines.insert(n, '')

    return lines


def preprocess(path):
    """Preprocesses path."""

    # Load and print the metadata.  Obfuscate the title field as a workaround
    # to a pandoc bug.  This gets undone py postprocess.py.
    meta = getmeta(path)
    printmeta(meta, obfuscate=True)

    # Read in the lines
    lines = getcontent(path)

    # Insert the image into the lines
    if meta['image'] and meta['showimage']:
        lines = insert_figure(lines, meta['image'], meta['caption'])

    # Replace the macros
    for i, line in enumerate(lines):

        # Clearing line break
        if line == '<!-- break -->':
            lines[i] = '<div style="clear: both; height: 0;"></div>'

        # Vertical space
        if line == '<!-- vspace -->':
            lines[i] = '<div style="clear: both; height: 3rem;"></div>'

    # Append a line indicating updates
    if meta['updated']:
        lines.append('')
        lines.append('*(Updated %s.)*' % meta['updated'])

    # Print out the new lines
    printcontent(lines)


if __name__ == '__main__':
    preprocess(sys.argv[1])
