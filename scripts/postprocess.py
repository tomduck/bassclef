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

"""postprocess.py - a pandoc html postprocessor.

  This script reads pandoc html from stdin, postprocesses it, and
  writes the result to stdout.
"""

from sys import stdin
import re


from util import config


def fix_bugs_in_old_pandoc(lines):
    """Fixes bugs found in old pandoc version used by Debian Jessie."""

    # Pandoc sometimes encodes html when it should not
    old = '&lt;span class=&quot;fa fa-envelope badge&quot;&gt;&lt;/span&gt;'
    new = '<span class="fa fa-envelope badge"></span>'
    for i, line in enumerate(lines):
        lines[i] = line.replace(old, new)

    return lines


def fix_bugs_in_new_pandoc(lines):
    """Fixes bugs found in newer versions of pandoc."""

    # Pandoc should not be html-encoding variable replacements in templates
    # (which it does on a random basis).  This prevents us from injecting html
    # into html templates!
    old = '&lt;a href=“'
    new = '<a href="'
    for i, line in enumerate(lines):
        lines[i] = line.replace(old, new)
    old = '”&gt;'
    new = '">'
    for i, line in enumerate(lines):
        lines[i] = line.replace(old, new)

    # Pandoc should not be treating numbers in headers as list items.  Here
    # we undo the temporary obfuscation made by preprocess.py's call to
    # util.getmeta().
    p = re.compile(r'<title>(\d+)// (.*?)</title>')
    for i, line in enumerate(lines):
        if p.search(line):
            num, title = p.search(line).groups()
            lines[i] = '<title>%s. %s</title>' % (num, title)
    p = re.compile(r'<meta (.*?) content="(\d+)// (.*?)" />')
    for i, line in enumerate(lines):
        if p.search(line):
            attrs, num, title = p.search(line).groups()
            lines[i] = '<meta %s content="%s. %s" />' % (attrs, num, title)
    p = re.compile(r'(\s+)<h1 (.*?)>(\d+)// (.*?)</h1>')
    for i, line in enumerate(lines):
        if p.search(line):
            spaces, attrs, num, title = p.search(line).groups()
            lines[i] = '%s<h1 %s>%s. %s</h1>' % (spaces, attrs, num, title)

    # Change <p><br /></p> to just <br />
    for i, line in enumerate(lines):
        lines[i] = line.replace('<p><br /></p>', '<br />\n')

    # Remove paragraph markers from <title> </title>
    for i, line in enumerate(lines):
        if line.strip().startswith('<title>'):
            lines[i] = line.replace('<p>', '').replace('</p>', '')
            break
        if line.strip().startswith('</head>'):
            break

    return lines


def adjust_urls(lines):
    """Put webroot/ into relative urls."""
    p = re.compile('((src|href)="/(.*?)")')
    for i, line in enumerate(lines):
        replace = False
        for group in p.findall(line):
            replace = True
            old, tag, path = group
            new = '%s="%s/%s"' % (tag, config('webroot'), path)
            line = line.replace(old, new)
        if replace:
            lines[i] = line
    return lines


def link_images(lines):
    """Link images to their full-size originals."""
    p = re.compile('(<img src="/(.*?)/images/(.*?)".*?/>)')
    for i, line in enumerate(lines):
        if p.search(line):
            # If this is already linked, don't do it again
            if line.strip().lower().endswith('</a>') or \
              lines[i+1].strip().lower().startswith('</a>'):
                continue
            imgtag, root, subpath = p.search(line).groups()
            # Don't link in originals
            if subpath.startswith('originals/'):
                continue
            linked_imgtag = '<a href="/%s/images/originals/%s">%s</a>' % \
              (root, subpath, imgtag)
            lines[i] = line.replace(imgtag, linked_imgtag)
    return lines


def open_tabs_when_clicked(lines):
    """Makes clicking links open tabs (for select cases)."""

    # Make social badge links open a new tab when clicked
    p = re.compile(r'(<a href="([^"]*?)"><span class="fa (.*?)">)')
    for i, line in enumerate(lines):
        if p.search(line):
            old, url, classes = p.search(line).groups()
            new = '<a href="%s" target="_blank"><span class="fa %s">' \
                  % (url, classes)
            lines[i] = line.replace(old, new)

    return lines


def generate_tooltips(lines):
    """Generates tooltips (for select cases)."""

    # Give social links a tooltip
    p = re.compile(r'(<a href="([^"]*?)" (.*?)><span class="fa (.*?)">)')
    for i, line in enumerate(lines):
        if p.search(line):
            old, url, attrs, classes = p.search(line).groups()

            if 'twitter' in url:
                title = 'Tweet this'
            elif 'facebook' in url:
                title = 'Share this on Facebook'
            elif 'google' in url:
                title = 'Share this on Google+'
            elif 'linkedin' in url:
                title = 'Share this on LinkedIn'
            elif 'mailto' in url:
                title = 'Share this by Email'
            else:
                continue
            new = '<a href="%s" %s title="%s"><span class="fa %s">' \
                  % (url, attrs, title, classes)

            lines[i] = line.replace(old, new)

    return lines


def tidy_html(lines):
    """Aesthetic improvements to pandoc's html output."""

    # Add some space around hr tags
    for i, line in enumerate(lines):
        lines[i] = line.replace('<hr />', '\n<hr />\n')

    # Don't separate </div> tags from their descriptions
    for i, line in enumerate(lines[:-1]):
        if line.startswith('</div>') and lines[i+1].startswith('<!--') \
            and lines[i+1].rstrip().endswith('-->'):
            lines[i] = lines[i][:-1] + ' ' + lines[i+1] + '\n'
            lines[i+1] = None
            continue
        if line.startswith('</div>') and lines[i+1].startswith('<p><!--') \
            and lines[i+1].rstrip().endswith('--></p>'):
            lines[i] = lines[i][:-1] + ' ' + lines[i+1][3:-5] + '\n'
            lines[i+1] = None
            continue
    lines = [line for line in lines if line is not None]

    # Put some space before the div content-body tag
    for i, line in enumerate(lines):
        if line.startswith('<div class="content-body">'):
            lines[i] = '\n' + line

    return lines


def postprocess():
    """Postprocesses html output piped from pandoc."""

    # Get the lines
    lines = [line for line in stdin]

    # Essential fixes
    lines = fix_bugs_in_old_pandoc(lines)
    lines = fix_bugs_in_new_pandoc(lines)
    lines = adjust_urls(lines)

    # Functionality enhancements
    lines = link_images(lines)
    lines = open_tabs_when_clicked(lines)
    lines = generate_tooltips(lines)

    # Aesthetic improvements to html
    lines = tidy_html(lines)

    # Print to stdout
    print(''.join(lines))


if __name__ == '__main__':
    postprocess()
