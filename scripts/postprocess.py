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

"""postprocess.py - a pandoc html postprocessor.

  Usage: preprocess.py src/.../filename.md

  This script reads pandoc html from stdin, postprocesses it, and
  writes the result to stdout.
"""

import sys
import re


from util import config

def postprocess():
    """Postprocesses output piped from pandoc."""

    # Get the lines
    lines = [line for line in sys.stdin]


    ## Essential fixes ##

    # Fix buggy output in old pandoc version used by Debian jessie
    old = '&lt;span class=&quot;fa fa-envelope badge&quot;&gt;&lt;/span&gt;'
    new = '<span class="fa fa-envelope badge"></span>'
    for i, line in enumerate(lines):
        lines[i] = line.replace(old, new)

    # Undo temporary changes made by util.metadata()
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


    ## Functionality fixes ##

    # Put webroot into image urls
    p = re.compile('((src|href)="/images/(.*?)")')
    for i, line in enumerate(lines):
        if p.search(line):
            old, tag, path = p.search(line).groups()
            new = '%s="%s/images/%s"' % (tag, config('webroot'), path)
            lines[i] = line.replace(old, new)

    # Link sized figure images to their larger versions
    p = re.compile('(<img src="/images/sized/(.*?)" (.*?) />)')
    for i, line in enumerate(lines):
        if p.search(line):
            old, img, attrs = p.search(line).groups()
            new = '<a href="/images/%s" %s >%s</a>' % (img, attrs, old)
            lines[i] = line.replace(old, new)

    # Make badge links open a new tab when clicked
    p = re.compile('(<a href="(.*?)"><span class="fa (.*?)">)')
    for i, line in enumerate(lines):
        if p.search(line):
            old, url, classes = p.search(line).groups()
            new = '<a href="%s" target="_blank"><span class="fa %s">' \
              % (url, classes)
            lines[i] = line.replace(old, new)


    ## Aesthetic fixes to html ##

    # Add some space around hr tags
    for i, line in enumerate(lines):
        lines[i] = line.replace('<hr />', '\n<hr />\n')

    # Don't separate /divs from their descriptions
    for i, line in enumerate(lines[:-1]):
        if line is None:
            continue
        if line.startswith('</div>') and lines[i+1].startswith('<!--'):
            lines[i] = lines[i][:-1] + ' ' + lines[i+1]
            lines[i+1] = None
            continue
        if line.startswith('</div>') and lines[i+1].startswith('<p><!--'):
            lines[i] = lines[i][:-1] + ' ' + lines[i+1][3:-5]
            lines[i+1] = None


    ## Output ##

    # Print to stdout
    lines = [line for line in lines if line != None]
    print(''.join(lines))


if __name__ == '__main__':
    postprocess()

