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

"""util.py - utility functions for use by bassclef's scripts."""

import configparser
import re
import string
from urllib.parse import urlencode, urljoin, urlparse
from sys import stdout
import os.path

import yaml


def config(key=None):
    """Returns the configuration as a dict.

    key - a single config item to return
    """

    # Read the config.ini into a dict, discarding the section info
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    cfg = {}
    for section in parser.sections():
        cfg.update({k:v for k, v in parser.items(section)})

    # Add the domain name and webroot for this site so that they may be used
    # by the template
    if 'siteurl' in cfg:

        # e.g., suppose siteurl is https://tomduck.github.io/bassclef/

        # The domain name of the site; e.g., tomduck.github.io
        cfg['domainname'] = urlparse(cfg['siteurl'])[1]

        # The web root for this site; e.g., /bassclef
        cfg['webroot'] = urlparse(cfg['siteurl'])[2]
        if cfg['webroot'].endswith('/'):
            cfg['webroot'] = cfg['webroot'][:-1]

    # Sanity checks
    if 'template' in cfg:
        assert cfg['template'].startswith('templates/') and \
          os.path.exists(cfg['template'])
    if 'twittername' in cfg:
        if cfg['twittername'].startswith('@'):
            cfg['twittername'] = cfg['twittername'][1:]
    if 'socialprofiles' in cfg:
        cfg['socialprofiles'] = ', '.join('"' + p.strip('" ') + '"' \
                  for p in cfg['socialprofiles'].split(','))

    # Return the config dict or a value if the key is given
    return cfg[key] if key else cfg


def getmeta(path, key=None):
    """Returns the metadata dict for the file at path.

    key - a single metadata item to return

    This reads the metadata from the file and combines it with the
    defaults in config.ini.
    """

    # Start with the config
    meta = config()

    with open(path) as f:

        # Check for a YAML block at the top of the file
        if f.readline().strip() != '---':
            return meta

        # Read in the metadata block
        lines = ['---']
        for line in f:
            line = line.rstrip()  # Must preserve leading spaces
            lines.append(line)
            if line.strip() == '...':  # Signifies end of the metadata block
                lines[-1] = '...'
                break

    # Check for the end of the metadata block
    if lines[-1] != '...':
        raise RuntimeError('End of YAML metadata block not found.')

    # Parse the metadata
    meta.update(yaml.load('\n'.join(lines)))

    # Sanity checks
    if 'template' in meta:
        assert meta['template'].startswith('templates/') and \
          os.path.exists(meta['template'])
    if 'image' in meta:
        assert meta['image'].startswith('/') \
               or meta['image'].startswith('http://') \
               or meta['image'].startswith('https://')

    # Inject bassclef's metadata fields
    meta['permalink'] = path2url(path, relative=True)
    meta['schemameta'] = _schemameta(meta)
    meta['ogmeta'] = _ogmeta(meta)
    meta['cardmeta'] = _cardmeta(meta)
    if 'title' in meta:
        meta['socialwidgets'] = _socialwidgets(meta['title'], path2url(path))

    # Return the meta dict or a value if key is given
    return meta[key] if key else meta


def printmeta(meta, f=stdout, obfuscate=False):
    """Prints the metadata dict as YAML to f.

    obfuscate - indicates that numbered titles should be obfuscated as
                a workaround to a bug in pandoc.
    """

    f.write('---\n')

    for k, v in meta.items():

        if v is None:
            continue

        if obfuscate and k == 'title':
            # Numbered titles get treated like lists by pandoc.  This messes
            # up the html meta fields.  Make a temporary and unobtrosive
            # change that we can undo in the postprocessing.
            p = re.compile(r'^(\d+)\. (.*)')
            if p.search(v):
                v = '%s// %s' % p.search(v).groups()

        if k in ['schemameta', 'ogmeta', 'cardmeta']:
            f.write('%s: >\n    %s\n' % (k, v.replace('\n', '\n    ')))
        elif v:  # Quote strings and write the result
            v = '"' + v.strip().replace('\n', '').replace('"', r'\"') + '"'
            f.write('%s: %s\n' % (k, v))  # Write the key, value pair


    f.write('...\n')


def getcontent(path):
    """Returns the content of a .md file as a list of lines."""

    with open(path) as f:

        # Skip the metadata
        if f.readline().strip() == '---':
            while f.readline().strip() != '...':
                continue
        else:
            f.seek(0)

        # Return the content
        return [line.rstrip() for line in f]


def printcontent(lines, f=stdout):
    """Prints the content to f."""
    f.write('\n'.join(lines))


def path2url(path, relative=False):
    """Converts a markdown path to the url generated from it.

    path - the path to convert
    relative - flags that the returned url should be relative; otherwise
               a fully-resolved url is returned
    """

    # Trim off the first directory and .in extension
    path = re.compile('/?.*?/(.*?.md)').search(path).groups()[0]
    path = path.replace('.md', '.html')  # Change the file extension
    if path.endswith('index.html'):  # Remove index.html
        path = path[:-10]
    if relative:
        return '/%s'%path
    else:
        return urljoin(config('siteurl'), path)


def _schemameta(meta):
    """Schema.org metadata (google): https://goo.gl/66WW3r"""

    lines = []
    lines.append('<!-- schema.org metadata (google): https://goo.gl/66WW3r -->')
    lines.append('<script type="application/ld+json">')
    lines.append('{')
    lines.append('  "@context" : "http://schema.org",')
    if 'schematype' in meta:
        lines.append('  "@type" : "%(schematype)s",')
    if 'schemaname' in meta:
        lines.append('  "name" : "%(schemaname)s",')
    if 'schemaurl' in meta:
        lines.append('  "url" : "%(schemaurl)s",')
    if 'socialprofiles' in meta:
        lines.append('  "sameAs" : [%(socialprofiles)s]')
    lines.append('}')
    lines.append('</script>')

    return '\n'.join(lines) % meta


def _ogmeta(meta):
    """OpenGraph metadata (facebook): http://ogp.me/"""

    lines = []
    lines.append('<!-- OpenGraph metadata (facebook): http://ogp.me/ -->')
    if 'title' in meta:
        lines.append('<meta property="og:title" content="%(title)s" />')
    if 'description' in meta:
        lines.append('<meta property="og:description" ' \
                     'content="%(description)s" />')
    elif 'subtitle' in meta:
        lines.append('<meta property="og:description" ' \
                     'content="%(subtitle)s" />')
    lines.append('<meta property="og:type" content="website" />')
    if 'permalink' in meta:
        lines.append('<meta property="og:url" content="%(permalink)s" />')
    if 'image' in meta:
        lines.append('<meta property="og:image" ' \
                     'content="http://%(domainname)s%(webroot)s%(image)s" />')

    return '\n'.join(lines) % meta


def _cardmeta(meta):
    """Card metadata (twitter): https://dev.twitter.com/cards/overview"""

    lines = []
    lines.append('<!-- Card metadata (twitter): '\
                 'https://dev.twitter.com/cards/overview -->')
    lines.append('<meta name="twitter:card" content="summary" />')
    if 'twittername' in meta:
        lines.append('<meta name="twitter:site" content="@%(twittername)s" />')
    if 'title' in meta:
        lines.append('<meta name="twitter:title" content="%(title)s" />')
    if 'description' in meta:
        lines.append('<meta name="twitter:description" ' \
                     'content="%(description)s" />')
    if 'subtitle' in meta:
        lines.append('<meta name="twitter:description" ' \
                     'content="%(subtitle)s" />')
    if 'image' in meta:
        lines.append('<meta name="twitter:image" ' \
                     'content="http://$domainname$$webroot$%(image)s" />')

    return '\n'.join(lines) % meta


def _socialwidgets(msg, url):
    """Returns html for social widgets.

    msg - the message to share
    url - the url to share
    """

    # Get the configuration
    cfg = config()

    # Create and return the widgets

    template = r'<li><a href="%(url)s"><span class="fa fa-%(service)s badge">'\
               '</span></a></li>'

    twitterdata = {'url':url, 'text':msg}
    if 'twittername' in cfg:
        twitterdata['via'] = cfg['twittername']
    twitter = template % {
        'service': 'twitter',
        'url': 'https://twitter.com/share?' + urlencode(twitterdata)
        }

    facebook = template % {
        'service': 'facebook',
        'url': 'http://www.facebook.com/sharer.php?' + urlencode({'u':url})
        }

    google = template % {
        'service': 'google-plus',
        'url': 'https://plus.google.com/share?' + urlencode({'url':url})
        }

    linkedin = template % {
        'service': 'linkedin',
        'url': 'http://www.linkedin.com/shareArticle?' + \
               urlencode({'mini': True, 'url':url})
        }

    email = template % {
        'service': 'envelope',
        'url': 'mailto:?' + \
               urlencode({'subject': msg, 'body': url}).replace('+', '%20')
        }

    return ''.join(['<ul>', twitter, facebook, google, linkedin, email, '</ul>'])

