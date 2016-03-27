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

"""util.py - utility functions for use by bassclef's scripts."""

import configparser
import re
import string
from urllib.parse import urlencode, urljoin, urlparse

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
    if 'twittername' in cfg:
        if cfg['twittername'].startswith('@'):
            cfg['twittername'] = cfg['twittername'][1:]

    # Return the config dict or a value if the key is given
    if key and key in cfg:
        return cfg[key]
    else:
        return cfg


def getmeta(path):
    """Returns the metadata dict for the file at path.

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

    # Check that the image url conforms
    if meta['image']:
        assert meta['image'].startswith('/') \
               or meta['image'].startswith('http://') \
               or meta['image'].startswith('https://')

    # Define both author and authors fields
    if 'authors' not in meta:
        meta['authors'] = meta['author']

    # Inject the social widgets
    meta['socialwidgets'] = _socialhtml(meta['title'], path2url(path)) \
      if meta['showtitle'] and meta['showsocial'] else ''

    # Add the permalink
    meta['permalink'] = path2url(path)

    # Ensure valid caption
    if meta['caption'] is None:
        meta['caption'] = ''

    return meta


def printmeta(meta, obfuscate=False):
    """Prints the metadata dict as YAML to stdout.

    obfuscate - indicates that numbered titles should be obfuscated as
                a workaround to a bug in pandoc.
    """

    print('---')

    for k, v in meta.items():

        if obfuscate and k == 'title':
            # Numbered titles get treated like lists by pandoc.  This messes
            # up the html meta fields.  Make a temporary and unobtrosive
            # change that we can undo in the postprocessing.
            p = re.compile(r'^(\d+)\. (.*)')
            if p.search(v):
                v = '%s// %s' % p.search(v).groups()

        print('%s: %s' % (k, v))

    print('...')


def skipmeta(f):
    """Skips the metadata at the beginning of the file f."""
    if f.readline().strip() == '---':
        while f.readline().strip() != '...':
            continue
    else:
        f.seek(0)
    return f


def get_content_body(htmlpath):
    """Returns lines for the content-body of an html file.

    This function searches for the following markers and returns everything
    in between:

      <div class="body">
      </div> <!-- class="body" -->
    """

    # Read and process each line
    with open(htmlpath) as f:
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


def _socialhtml(msg, url):
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

    return '\n'.join(['<div class="social">', '<ul>',
                      twitter, facebook, google, linkedin, email,
                      '</ul>', '</div> <!-- class="social" -->\n'])
