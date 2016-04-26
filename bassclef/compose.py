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

"""compose.py - assembles markdown from a .md.in file"""

import sys
from sys import stdout
import os, os.path
import re
import tempfile
import subprocess

from bassclef.util import getmeta, printmeta, getcontent, printcontent, path2url


# pylint: disable=too-many-locals
def process(lines, meta, n):
    """Processes the content lines of a markdown file.

    Footnotes are eliminated and links are namespaced in order to avoid
    collisions.  The markdown is truncated where <!-- cut --> is found, and
    a "Read more..." line is added.
    """

    # Link reference and definition patterns
    p1 = re.compile(r'(\[(.*?)\]\[(?!%d:)(.*?)\])'%n)  # Reference
    p2 = re.compile(r'^\[(?!\^)(.*?)\]:')              # Definition

    # Footnote reference and definition patterns
    p3 = re.compile(r'(?!^)(\[\^(.*?)\])')             # Reference
    p4 = re.compile(r'^(\[\^(.*?)\]:)')                # Definition

    cutpoint = False  # Flags that a cut point was found
    lastline = None   # Track the last line
    innote = False    # Flags we are in a footnote definition
    out = []          # The list of processed lines

    # Read, process, and store each line
    for line in lines:

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

        # Check if we are in a footnote definition
        if innote:
            if lastline == '' and line and not line.startswith('    '):
                innote = False
        elif p4.search(line):
            innote = True

        # Store the line.  Ignore all footnotes, and ignore markdown after
        # <!-- cut --> except for link references.
        if (not innote and not cutpoint) or p2.search(line):
            out.append(line)

        # Remember the last line
        lastline = line

    # Add a 'Read more...' link if <!-- cut --> was found.
    if cutpoint:
        out.append('\n[Read more...](%s)\n'%meta['permalink'])

    # Return the processed lines
    return out


def content_printer():
    """Prints the processed content of a .md file to stdout.

    Use it this way:

      printer = content_printer()
      next(printer)
      printer.send('/path/to/file.md')

    Send as many paths as you want.

    The content is processed internally and by pandoc (via a system call).
    The output is html.  For any subsequent processing with pandoc, don't
    forget to turn off its markdown_in_html_blocks extension.
    """

    # Keep track of the number of files processed
    n = 0

    while True:

        # Get the next path
        path = yield

        # Print a horizontal rule between files
        if n != 0:
            print('\n<hr />\n')

        # Read and process the file
        meta = getmeta(path)
        lines = process(getcontent(path), meta, n)

        # Flag the first entry in the metadata
        meta['first-entry'] = True if n == 0 else False

        # Write the markdown to a temporary file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            path = f.name
            printmeta(meta, f=f)
            printcontent(lines, f=f)

        # Process the markdown with pandoc, printing the output to stdout
        stdout.flush()
        subprocess.call(['pandoc', path, '-s', '-S', '-thtml5',
                         '--template=templates/entry.html5'])
        stdout.flush()

        # Print a newline at the end of pandoc's output
        print('')

        # Remove the temporary file
        os.remove(path)

        # Increment the counter
        n += 1


def compose(path=sys.argv[1]):
    """Composes the .md.in file at path."""

    assert path.startswith('markdown/')

    meta = getmeta(path)

    # Add to the metadata
    if meta['showrss']:
        url = path2url(path, relative=True)
        if not path.endswith('.html'):
            url = os.path.join(url, 'index.html')
        # pylint: disable=no-member
        meta['rssurl'] = url.replace('.html', '.xml')

    # Print the metadata to stdout
    printmeta(meta)

    # Read the lines of the .md.in file
    lines = getcontent(path)

    # Process the lines
    printer = content_printer()
    next(printer)
    for line in lines:
        # If a filename is given then print the file (subject to some
        # processing); otherwise, print the line as-is.
        if line.endswith('.md') and os.path.isfile(line):
            printer.send(line)
        else:
            print(line)

if __name__ == '__main__':
    compose()
