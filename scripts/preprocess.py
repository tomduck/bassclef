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

from urllib.parse import urljoin

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
    n = n if n is not None else len(lines)
    lines.insert(n, '\n![%s](%s)\n' % (caption, image))
    lines.insert(n, '')

    return lines


def preprocess(path):
    """Preprocesses path."""

    # Preload the metadata
    with open(path) as f:
        meta = metadata(f)

    # Extract the metadata fields we need
    title = meta['title'] if 'title' in meta else None
    authors = meta['author'] if 'author' in meta else \
      meta['authors'] if 'authors' in meta else None
    updated = meta['updated'] if 'updated' in meta else None
    image = meta['image'] if 'image' in meta else None
    showimage = meta['showimage'] if 'showimage' in meta else True
    caption = meta['caption'] if 'caption' in meta else ''
    showtitle = meta['showtitle'] if 'showtitle' in meta else True
    showsocial = meta['showsocial'] if 'showsocial' in meta else True

    # Get the social widgets
    if showtitle and showsocial:
        socialwidgets = '\n'.join(social(title, path2url(path)))
    else:
        socialwidgets = ''

    with open(path) as f:

        # Load the metadata
        defaults = {'titleclass':'title',
                    'authors':authors,
                    'showtitle': True,
                    'permalink':path2url(path),
                    'socialwidgets':socialwidgets}
        meta = metadata(f, defaults, printmeta=True)

        # Read in the lines
        lines = [line.rstrip() for line in f]

    # Insert the image into the lines
    if image and showimage:
        lines = insert_figure(lines, image, caption)

    # Append a line indicating updates
    if updated:
        lines.append('')
        lines.append('*(Updated %s.)*' % updated)

    # Print out the new lines
    print('\n'.join(lines))


if __name__ == '__main__':
    preprocess(sys.argv[1])
