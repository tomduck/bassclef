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

  Usage: compose.py markdown/.../filename.md.in

  This script reads a .md.in file and writes a .md file to stdout.  Filenames
  listed alone on a line are read, processed, and inserted.  Other elements
  are left untouched.
"""

import sys
import os.path
import re
import tempfile
import subprocess

from util import getmeta, printmeta, getcontent, printcontent, path2url


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

    cutpoint = False    # Flags that a cut point was found
    out = []            # The list of processed lines

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

        # Store the line.  Ignore all footnotes, and ignore markdown after
        # <!-- cut --> except for link references.
        if (not p4.search(line) and not cutpoint) or p2.search(line):
            out.append(line)

    # Add a 'Read more...' link if <!-- cut --> was found.
    if cutpoint:
        out.append('\n[Read more...](%s)\n'%meta['permalink'])

    # Return the processed lines
    return out


def content_printer():
    """Prints the processed content of a .md file to stdout.

    Use it this way:

      printer = md_content_printer()
      printer.send('/path/to/file.md')

    Send as many paths as you want.

    The content is processed internally and by pandoc (via a system call).
    The output is html.  For any subsequent processing with pandoc, don't
    forget to turn off its markdown_in_html_blocks extension.
    """

    # Keep track of the number of files processed
    n = 0

    while True:

        # Print a horizontal rule between files
        if n != 0:
            print('\n<hr />\n')

        # Get the next path
        path = yield

        # Read and process the file
        meta = getmeta(path)
        lines = process(getcontent(path), meta, n)

        # Write the markdown to a temporary file and process it with pandoc.
        # The temporary file is automatically deleted at the end.
        with tempfile.NamedTemporaryFile() as f:

            # Write the markdown
            printmeta(meta, f=f)
            printcontent(lines, f=f)

            # Process it the markdown with pandoc, printing the output to stdout
            subprocess.call(['pandoc', f.name, '-s', '-S', '-t html5',
                             '--template ../templates/entry.html5'])


def compose(path):
    """Composes the .md.in file at path."""

    assert path.startswith('markdown/')

    meta = getmeta(path)

    # Add the rss url to the metadata
    if meta['showrss']:
        url = path2url(path, relative=True)
        if not path.endswith('.html'):
            url = os.path.join(url, 'index.html')
        meta['rssurl'] = url.replace('.html', '.xml')

    # Print the metadata to stdout
    printmeta(meta)

    # Read the lines of the .md.in file
    lines = getcontent(path)

    # Process the lines
    printer = content_printer()
    for line in lines:
        # If a filename is given then print the file (subject to some
        # processing); otherwise, print the line as-is.
        if line.endswith('.md') and os.path.isfile(line):
            printer.send(line)
        else:
            print(line)

if __name__ == '__main__':
    compose(sys.argv[1])
