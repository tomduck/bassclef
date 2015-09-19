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

"""compose.py - assembles pandoc markdown from a .md.in file.

  Usage: compose.py content/.../filename.md.in

  This script reads a .md.in file and writes a .md file to stdout.  Filenames
  listed alone on a line are read, processed, and inserted.  Other elements
  are left untouched.
"""

import sys
import os.path
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
    """Returns lines for the content of a .md file.

    The content is truncated where <!-- break --> is found.
    """

    refpatt = re.compile(r'^\[.*?]:')  # Link reference pattern

    breakpoint = False  # Flags that a break point was found
    lines = []          # The list of processed lines


    # Read, process, and store each line
    for line in f:

        # Strip whitespace at the ends
        line = line.strip()

        # Use the number n to give each link and reference a namespace
        line = line.replace('][', ']['+str(n)+':')
        if refpatt.search(line):
            line = '['+str(n)+':'+line[1:]

        # Check for a break point
        if line == '<!-- break -->':
            breakpoint = True

        # Store the line.  Cut out all content after <!-- break --> except
        # for references.
        if not breakpoint or refpatt.search(line):
            lines.append(line)


    # Add a 'Read more...' link if <!-- break --> was found.
    if breakpoint:
        lines.append('\n[Read more...](%s)\n'%url)

    # Return the processed lines
    return lines


def process_md_file(path, n):
    """Processes a .md file.

    n - a unique file number used for namespacing; it must be 0 for the
        first file.
    """

    # Print a horizontal rule between files
    if n != 0:
        print('\n<hr />\n')

    # Get the url
    url = path2url(path, relative=True)

    # Read, process and print the file
    with open(path) as f:

        # Retrieve the metadata
        meta = metadata(f)

        # Title block
        print('\n'.join(titleblock(meta, url)))

        # Social widgets
        is_social = meta['social'] if 'social' in meta else True
        if is_social and 'title' in meta:
            print('\n'.join(social(meta['title'], path2url(path))))

        # Content
        print('\n'.join(content(f, url, n)))


def process_mdin_file(path):
    """Processes the .md.in file at path."""

    assert path.startswith('content/')

    # Read in the metadata and lines
    with open(path) as f:

        # Load the metadata
        update = {'titleclass':'section', 'permalink':path2url(path)}
        metadata(f, update, printmeta=True)

        # Get the remaining lines
        lines = [line.strip() for line in f if len(line.strip())]


    # Process the lines
    n = 0  # Used to provide a unique namespace for each file
    for line in lines:

        # Strip away whitespace at ends
        line = line.strip()

        # If a filename is given then read, process, and print the file;
        # otherwise, print the line as-is.
        if os.path.isfile(line):
            process_md_file(path, n)
            n += 1
        else:
            print(line)


if __name__ == '__main__':
    process_mdin_file(sys.argv[1])
