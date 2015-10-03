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

    The content is truncated where <!-- cut --> is found.
    """

    # Reference and link patterns
    p1 = re.compile(r'(\[(.*?)\]\[(?!%d:)(.*?)\])'%n)
    p2 = re.compile(r'^\[(?!\^)(.*?)\]:')

    # Reference and footnote patterns
    p3 = re.compile(r'(?!^)(\[\^(.*?)\])')
    #p4 = re.compile(r'^(\[\^(.*?)\]:)')

    cutpoint = False    # Flags that a cut point was found
    lines = []          # The list of processed lines


    # Read, process, and store each line
    for line in f:

        # Strip whitespace at the right end
        line = line.rstrip()

        # Use the number n to give links a namespace
        while p1.search(line):
            old, a, b = p1.search(line).groups()
            new = '[%s][%d:%s]'%(a, n, b)
            line = line.replace(old, new)
        if p2.search(line):
            a = p2.search(line).groups()[0]
            line = p2.sub('[%d:%s]:'%(n, a), line)

        # Strip footnote references
        if p3.search(line):
            a = p3.search(line).groups()[0]
            line = p3.sub('', line)

        # Check for a cut point
        if line == '<!-- cut -->':
            cutpoint = True

        # Store the line.  Ignore all content after <!-- cut --> except
        # for references.
        if not cutpoint or p2.search(line):
            lines.append(line)


    # Add a 'Read more...' link if <!-- cut --> was found.
    if cutpoint:
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
        showsocial = meta['showsocial'] if 'showsocial' in meta else True
        if showsocial and 'title' in meta:
            print('\n'.join(social(meta['title'], path2url(path))))

        # Content
        print('\n'.join(content(f, url, n)))


def process_mdin_file(path):
    """Processes the .md.in file at path."""

    assert path.startswith('content/')

    # Construct the rss url
    rssurl = path2url(path, relative=True)
    if not path.endswith('.html'):
        rssurl = os.path.join(rssurl, 'index.html')
    rssurl = rssurl.replace('.html', '.xml')

    # Read in the metadata and lines
    with open(path) as f:

        # Load the metadata
        update = {'titleclass':'section',
                  'permalink':path2url(path),
                  'rssurl':rssurl}
        metadata(f, update, printmeta=True)

        # Get the remaining lines
        lines = [line.rstrip() for line in f if len(line.rstrip())]


    # Process the lines
    n = 0  # Used to provide a unique namespace for each file
    for line in lines:

        # Strip away whitespace at the right end
        line = line.rstrip()

        # If a filename is given then read, process, and print the file;
        # otherwise, print the line as-is.
        if line.endswith('.md') and os.path.isfile(line):
            process_md_file(line, n)
            n += 1
        else:
            print(line)


if __name__ == '__main__':
    process_mdin_file(sys.argv[1])
