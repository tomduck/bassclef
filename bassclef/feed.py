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

"""feed.py - creates an RSS 2 feed."""

import os
import datetime

import PyRSS2Gen as rss2

from bassclef.util import getmeta, getcontent, write, permalink

from html.entities import codepoint2name


def encode(txt):
    """Encodes UTF-8 characters with html entities."""
    skip = ['<', '>', '"', '&']
    ret = ''
    for c in txt:
        if c not in skip and ord(c) in codepoint2name:
            ret += "&" + codepoint2name.get(ord(c)) + ";"
        else:
            ret += c
    return ret


def get_content_body(htmlpath):
    """Returns lines for the content-body of an html file.

    This function searches for the following markers and returns everything
    in between except for the social widgets:

      <div class="content-body">
      </div> <!-- class="content-body" -->
    """

    # Read and process each line
    with open(htmlpath) as f:
        lines = []
        inbody = False    # Flags when we are in the content-body
        insocial = False  # Flags when we are in the social widget html
        for line in f:
            if '<div class="content-body">' in line:
                inbody = True
            if inbody:
                if '<div class="social">' in line:
                    insocial = True
                if not insocial:
                    lines.append(line)
                if '</div> <!-- class="social" -->' in line:
                    insocial = False
            if '</div> <!-- class="content-body" -->' in line:
                return '\n'.join(lines)

    raise RuntimeError('content-body not found')


def make_item(path):
    """Makes an item from .md file at path and its associated .html file."""

    assert path.startswith('markdown/') and path.endswith('.md')

    # Read and process the .md file
    meta = getmeta(path)

    # Get the permalink and guid
    plink = permalink(path[8:].replace('.md', '.html'))
    guid = rss2.Guid(plink)

    # Get the metadata
    pubdate = meta['date'] if 'date' in meta else None
    author = meta['author'] if 'author' in meta else None
    publisher = meta['publisher'] if 'publisher' in meta else None
    source = meta['source'] if 'source' in meta else None

    # Construct the item source
    source = rss2.Source(publisher, source) if publisher and source else None

    # Get the html body
    path = path.replace('.md', '.html')
    path = path.replace('markdown', 'www')
    description = encode(get_content_body(path))

    # Style the figure caption
    description = description.replace('<figcaption>',
                                      '<figcaption style="font-size: 80%;">')

    return rss2.RSSItem(title=meta['title'], link=plink, pubDate=pubdate,
                        author=author, source=source, description=description,
                        guid=guid)


def feed(args):
    """Makes a feed from an .md.in file."""

    path = args.path

    # Extract the metadata fields we need
    meta = getmeta(path)
    title = meta['rsstitle'] if 'rsstitle' in meta else None
    subtitle = meta['subtitle'] if 'subtitle' in meta else ''

    # Get the first ten RSS items from file listing at path
    lines = getcontent(path)
    items = [make_item(line.strip()) for line in lines \
             if line.strip().endswith('.md') and \
             os.path.isfile(line.strip())][:10]

    # Create the RSS
    rss = rss2.RSS2(generator=None,
                    docs=None,
                    title=title,
                    link=permalink(path[8:].replace('.md.in', '.html')),
                    description=subtitle,
                    lastBuildDate=datetime.datetime.now(),
                    items=items)

    # Write it out
    write(rss.to_xml())
