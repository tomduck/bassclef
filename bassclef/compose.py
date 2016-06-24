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
import os, os.path
import re
import tempfile
import subprocess
import uuid
import urllib.parse

from bassclef.util import getmeta, writemeta, getcontent, \
     writelines, write, permalink, STDOUT

import pandoc_tpp


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
        if line.strip() == '<!-- cut -->':
            cutpoint = True
            line = '\n'

        # Check if we are in a footnote definition
        if innote:
            if lastline.strip() == '' and line and not line.startswith('    '):
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


def content_writer():
    """Writes the processed content of a .md file to stdout.

    Use it this way:

      writer = content_writer()
      next(writer)
      writer.send('/path/to/file.md')

    Send as many paths as you want.

    The content is processed internally and by pandoc (via a system call).
    The output is html.  For any subsequent processing with pandoc, don't
    forget to turn off its markdown_in_html_blocks extension.
    """

    # Process the entry template with pandoc-tpp and write it to a
    # temporary file.  Remove leading spaces so that this can be written into
    # a markdown file.
    lines = pandoc_tpp.preprocess('templates/entry.html5')
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.html5',
                                     delete=False) as f:
        template_path = f.name
        f.writelines(lines)
    
    # Keep track of the number of files processed
    n = 0

    while True:

        # Get the path to the next entry
        path = yield
        assert path.startswith('markdown/')

        # Get various types of links
        rellink = path[8:-3] + '.html'
        plink = permalink(rellink)
        quoted_plink = urllib.parse.quote(plink).replace('/', '%2F')
            
        # Renew the entry's metadata
        meta = getmeta(path)
        meta['rellink'] = rellink
        meta['permalink'] = plink

        # Flag the first entry in the metadata
        if n == 0:
            meta['first-entry'] = 'True'
        elif 'first-entry' in meta:
            del meta['first-entry']

        # Process the entry's content
        lines = process(getcontent(path), meta, n)

        # Write the markdown to a temporary file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            tmppath = f.name
            writemeta(meta, f=f)
            writelines(lines, f=f)

        # Write a horizontal rule between files
        if n != 0:
            write('\n<hr />\n')

        # Start the new entry
        write('\n')
        write('<div id="entry-%d">\n'%n)

        # Process the markdown with pandoc, writing the output to stdout
        STDOUT.flush()
        assert path.startswith('markdown/') and path.endswith('.md')
        subprocess.call(['pandoc', tmppath,
                         '-s', '-S',
                         '-f', 'markdown+markdown_attribute',
                         '-t', 'html5',
                         '--email-obfuscation', 'none',
                         '--template', template_path,
                         '-M', 'permalink=' + plink,
                         '-M', 'quoted-permalink=' + quoted_plink])
        STDOUT.flush()

        write('</div> <!-- id="entry-%d" -->\n'%n)

        # Increment the counter
        n += 1


def compose(args):
    """Composes the .md.in file at path."""

    path = args.path

    meta = getmeta(path)
    meta['no-social'] = 'True'
    writemeta(meta)

    # Read the lines of the .md.in file
    lines = getcontent(path)

    # Process the lines
    writer = content_writer()
    next(writer)
    for line in lines:
        # If a filename is given then write the file (subject to some
        # processing); otherwise, write the line as-is.
        if line.strip().endswith('.md') and os.path.isfile(line.strip()):
            writer.send(line.strip())
        else:
            write(line)

if __name__ == '__main__':
    compose()
