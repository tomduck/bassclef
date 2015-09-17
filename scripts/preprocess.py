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

  Usage: preprocess.py content/.../filename.md

  This script reads in a pandoc markdown file, preprocesses it, and writes
  the result to stdout.
"""

import sys

from util import metadata, path2url, social


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

    # Look for the break line
    if n is None:
        flag = False  # Flag when we have found it
        for i, line in enumerate(lines):
            if flag:
                n = i
                break
            if line == '<!-- break -->':
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
    assert n is not None
    lines.insert(n, '\n![%s](%s)\n' % (caption, image))
    lines.insert(n, '')

    return lines


def preprocess(path):
    """Preprocesses the title file at path."""

    with open(path) as f:

        # Load the metadata
        meta = metadata(f, printmeta=True, permalink=path2url(path))

        # Read in the lines
        lines = [line.strip() for line in f]


    # Extract metadata fields we need to deal with
    updated = meta['updated'] if 'updated' in meta else None
    image = meta['image'] if 'image' in meta else None
    caption = meta['caption'] if 'caption' in meta else ''


    # Insert the image
    if image:
        lines = insert_figure(lines, image, caption)


    # Insert the social widgets
    if 'title' in meta:
        is_social = meta['social'] if 'social' in meta else True
        if is_social:
            lines.insert(0, '\n'.join(social(meta['title'], path2url(path))))
        else:
            lines.insert(0, '<p></p>')

    # Append a line indicating updates
    if updated:
        lines.append('')
        lines.append('*(Updated %s.)*' % updated)


    # Print out the new lines
    print('\n'.join(lines))


if __name__ == '__main__':
    preprocess(sys.argv[1])
