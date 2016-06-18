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

"""preprocess.py - pandoc markdown preprocessing"""


from bassclef.util import getmeta, writemeta, getcontent, writelines


def insert_figure(lines, image, caption):
    """Inserts a figure into the markdown lines."""

    # Look for the <!-- image --> processing flag
    n = None
    for i, line in enumerate(lines):
        if line.strip() == '<!-- image -->':
            n = i
            lines.pop(n)  # Remove the flag
            continue

    if n is None:
        # Find the end of the first paragraph
        flag = False  # Flags we have found the first paragraph
        for i, line in enumerate(lines):
            if not flag and line.strip():  # Leading blank lines
                flag = True
            if flag and not line.strip():  # First blank line after paragraph
                break
        n = i+1

    # Insert the lines for the figure
    lines.insert(n, '![%s](%s)\n' % (caption, image))
    lines.insert(n+1, '\n')

    return lines


def preprocess(args):
    """Preprocesses path."""

    path = args.path

    # Load and write the metadata.  Obfuscate the title field as a workaround
    # to a pandoc bug.  This gets undone by postprocess.py.
    meta = getmeta(path)
    writemeta(meta, obfuscate=True)

    # Read in the lines
    lines = getcontent(path)

    # Insert the image into the lines
    if 'image' in meta:
        caption = meta['caption'] if 'caption' in meta else ''
        lines = insert_figure(lines, meta['image'], caption)

    # Replace the processing flags
    for i, line in enumerate(lines):

        # Clearing line break
        if line.strip() == '<!-- break -->':
            lines[i] = '<div style="clear: both; height: 0;"></div>\n'

        # Vertical space
        if line.strip() == '<!-- vspace -->':
            lines[i] = '<div style="clear: both; height: 3rem;"></div>\n'

    # Write out the new lines
    writelines(lines)
