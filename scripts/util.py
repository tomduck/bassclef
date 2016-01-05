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

"""util.py - functions for use by bassclef scripts."""

import configparser
import re
import string
from urllib.parse import urlencode, urljoin, urlparse
from html.entities import codepoint2name

import yaml


def config(field=None):
    """Returns the configuration as a dict.

    field - if this is defined, return only this item; useful for shell
            programming.
    """

    # Read the config.ini into a dict (ignoring the sections)
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    cfg = {}
    for section in parser.sections():
        cfg.update({k:v for k, v in parser.items(section)})


    # Add some new configuration entries to the dict based on the config.ini
    if 'siteurl' in cfg:

        cfg['domainname'] = urlparse(cfg['siteurl'])[1]

        webroot = urlparse(cfg['siteurl'])[2]
        cfg['webroot'] = webroot[:-1] if webroot.endswith('/') else webroot


    # Sanity checks
    if 'twittername' in cfg:
        if cfg['twittername'].startswith('@'):
            cfg['twittername'] = cfg['twittername'][1:]

    if field in cfg:
        return cfg[field]
    else:
        return cfg

# pylint: disable=too-many-branches
def metadata(f, defaults=None, printmeta=False):
    """Returns the metadata from the top of a markdown file.

    defaults - default metadata for missing fields
    printmeta - flags that the lines should be printed to stdout
    """

    # Check for a YAML block at the top of the file
    if f.readline().strip() != '---':
        raise RuntimeError('YAML metadata block not found.')

    # Read in the metadata
    lines = ['---']
    for line in f:
        line = line.rstrip()  # Must preserve leading spaces
        lines.append(line)
        if line == '...':  # Signifies end of the metadata block
            break

    # Check for the end of the metadata block
    if lines[-1] != '...':
        raise RuntimeError('End of YAML metadata block not found.')

    # Insert config variables as metadata
    for k, v in config().items():
        lines.insert(-1, '%s: %s'%(k, v))

    # Insert the defaults as metadata.  Check with the existing meta first so
    # that we don't overwrite anything.
    meta = yaml.load('\n'.join(lines))
    if defaults:
        for k, v in defaults.items():
            if k == 'socialwidgets':
                # Must use a multi-line item here because the social widgets
                # html includes colons and quotes
                lines.insert(-1, '%s: >\n    %s'%\
                             (k, v.rstrip().replace('\n', '\n    ')))
            elif k not in meta:
                lines.insert(-1, '%s: %s' % (k, v))

    # Combine author and authors fields into one
    if 'author' in meta and 'authors' not in meta:
        lines.insert(-1, 'authors: %s' % meta['author'])

    # Parse the metadata and check it for errors
    meta = yaml.load('\n'.join(lines))
    for k, v in meta.items():
        if k == 'image':
            assert v.startswith('/') or v.startswith('http://')

    # Print the metadata to stdout
    if printmeta:

        p = re.compile(r'^title: (\d+)\. (.*)')

        for line in lines:

            # Numbered titles get treated like lists by pandoc.  This messes
            # up the html meta fields.  Make a temporary and unobtrosive
            # change that we can undo in the postprocessing.
            if p.search(line):
                pre, post = p.search(line).groups()
                print('title: %s// %s' % (pre, post))
                continue

            print(line)

    # Return the metadata
    return yaml.load('\n'.join(lines))


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


def html(htmlpath):
    """Returns lines for the body of an html file."""

    with open(htmlpath) as f:
        # Read and process each line
        lines = []
        flag = False
        for line in f:
            if line.startswith('<div class="body">'):
                flag = True
            if flag:
                lines.append(line)
            if line.startswith('</div> <!-- class="body" -->'):
                return '\n'.join(lines)


def path2url(path, relative=False):
    """Converts a markdown path to a www html url.

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
        return urljoin(config()['siteurl'], path)


def social(msg, url):
    """Returns html for social widgets.

    msg - the message to share
    url - the url to share
    """

    # Append a period to the end of the message (if needed)
    msg = msg if msg[-1] in string.ascii_letters + string.digits else msg + '.'

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

    return '<div class="social">\n<ul>',\
      '\n'.join([twitter, facebook, google, linkedin, email]),\
      '</ul>\n</div> <!-- class="social" -->\n'
