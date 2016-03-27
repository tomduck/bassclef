#! /usr/bin/env python3

"""feed.py - creates an RSS 2 feed."""

import sys, os
import datetime

import PyRSS2Gen as rss2

from util import metadata, path2url, html

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


def make_item(path):
    """Makes an item from .md file at path and its associated .html file."""

    # Read and process the .md file
    with open(path) as f:
        meta = metadata(f)

    # Get the link and guid
    link = path2url(path)
    guid = rss2.Guid(path2url(path, relative=False))

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
    description = encode(html(path))

    # Style the figure caption
    description = description.replace('<figcaption>',
                                      '<figcaption style="font-size: 80%;">')

    return rss2.RSSItem(title=meta['title'], link=link, pubDate=pubdate,
                        author=author, source=source, description=description,
                        guid=guid)


def process_mdin_file(path):
    """Processes the .md.in file at path."""

    assert path.startswith('markdown/')

    # Read in the metadata and lines
    with open(path) as f:

        # Load the metadata and lines
        meta = metadata(f)
        lines = [line.strip() for line in f]

    # Get the last ten items
    items = [make_item(line) for line in lines \
             if line.endswith('.md') and os.path.isfile(line)]
    items = items[:10] if len(items) > 10 else items

    # Extract the metadata fields we need
    title = meta['rsstitle'] if 'rsstitle' in meta else None
    subtitle = meta['subtitle'] if 'subtitle' in meta else ''

    rss = rss2.RSS2(generator=None,
                    docs=None,
                    title=title,
                    link=path2url(path, relative=False),
                    description=subtitle,
                    lastBuildDate=datetime.datetime.now(),
                    items=items)

    rss.write_xml(sys.stdout)


if __name__ == '__main__':
    process_mdin_file(sys.argv[1])

