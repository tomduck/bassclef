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

"""makesection.py - assembles pandoc markdown from a .md.in file.

  Usage: makesection.py content/.../filename.md.in

  This script reads a .md.in file and writes a .md file to stdout.  The
  input file must have YAML metadata that defines the section name.  The
  metadata should be followed by a list of files to include in the output
  (after some processing).
"""

import sys
import re

from util import metadata, path2url, social


def titleblock(meta, url):
    """Returns lines for a title block."""

    lines = ['\n<div class="titleblock">']

    # Get the dateline
    if 'date' in meta:
        html = '###### %(date)s'
        if 'publisher' in meta:
            if 'url' in meta:
                html += '['
            html += ', published in %(publisher)s'
        if 'url' in meta:
            html += '](%(url)s)'
        html += '###### {.dateline}'
        lines.append(html % meta)

    # Get the title
    if 'title' in meta:
        lines.append('# [%s](%s) # {.title}' % (meta['title'], url))

    # Get the subtitle
    if 'subtitle' in meta:
        lines.append('#### %(subtitle)s #### {.subtitle}' % meta)

    lines.append('</div> <!-- class="titleblock" -->')

    return lines


def content(f, url, n):
    """Returns lines for the content."""

    refpatt = re.compile(r'^\[.*?\]:')  # Link reference pattern
    breakpoint = False  # Flags when breakpoint found
    lines = []

    for line in f:
        line = line.strip()

        # Print out any references that are found.  Put the file number
        # in the reference in order to avoid collisions.
        if refpatt.search(line):
            lines.append('['+str(n)+':'+line[1:])
            continue

        # Check for a break point
        if line == '<!-- break -->':
            breakpoint = True

        # Print out lines unless the break point was found.  Put the
        # file number in the reference as above.
        if not breakpoint:
            lines.append(line.replace('][', ']['+str(n)+':'))

    if breakpoint:
        lines.append('\n[Read more...](%s)\n'%url)

    return lines


def process_title_file(path, n):
    """Processes the title file using the current, previous and next paths.

    n - a unique file number; must be 0 for the first file
    """

    # Print a rule between files
    if n != 0:
        print('\n<hr />\n')

    # Get the url
    url = path2url(path, relative=True)

    # Read in file and print each line until the break line
    with open(path) as f:

        # Retrieve the metadata
        meta = metadata(f)

        # Title block
        print('\n'.join(titleblock(meta, url)))

        # Social widgets
        if 'title' in meta:
            print('\n'.join(social(meta['title'], path2url(path))))

        # Content
        print('\n'.join(content(f, url, n)))


def process_section_file(path):
    """Processes the section file at path."""

    assert path.startswith('content/')

    # Process the section file
    with open(path) as f:

        # Load the metadata
        meta = metadata(f, printmeta=True, permalink=path2url(path))
        assert 'section' in meta

        # Get the paths to the title files
        paths = [line.strip() for line in f if len(line.strip())]


    # Process each title file
    for n, path in enumerate(paths):
        process_title_file(path, n)


if __name__ == '__main__':
    process_section_file(sys.argv[1])
