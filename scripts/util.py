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

import string
import yaml
from urllib.parse import urlencode, urljoin


def config():
    """Returns the configuration as a dict."""

    # Read the configuration into a dict
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    cfg = {}
    for section in parser.sections():
        cfg.update({k:v for k, v in parser.items(section)})

    # Sanity checks
    if 'twittername' in cfg:
        if cfg['twittername'].startswith('@'):
            cfg['twittername'] = cfg['twittername'][1:]

    return cfg


def metadata(f, printmeta=False, permalink=None):
    """Returns the metadata and lines from the top of a markdown file."""

    # Make sure there is a YAML block at the top of the file
    if f.readline().strip() != '---':
        raise RuntimeError('Expected YAML metadata at top of file')

    # Read in and parse the metadata
    lines = ['---\n']
    for line in f:
        lines.append(line)
        if line.startswith('...'):
            break

    # Insert config entries as metadata
    for k, v in config().items():
        lines.insert(-1, '%s: %s\n'%(k, v))

    # Insert permalink as metadata
    if permalink:
        lines.insert(-1, 'permalink: %s\n'%permalink)

    lines = ''.join(lines)

    # Print the metadata out if requested
    if printmeta:
        print(lines)

    # Parse and return the metadata and lines
    return yaml.load(lines)


def path2url(path, relative=False):
    """Converts a markdown source path to a www html url.

    path - the path to convert.
    relative - flags whether the returned url should be relative
               (versus absolute).
    """
    assert path.startswith('content/') or path.startswith('tmp/')
    path = path[path.index('/')+1:]  # Trim off content/ or tmp/ from the path
    if path.endswith('.in'):  # Trim off .in extension
        path = path[:-2]
    path = path.replace('.md', '.html')  # Change the file extension
    if path.endswith('index.html'):  # Remove index.html
        path = path[:-10]
    if relative:
        return '/%s'%path
    else:
        return urljoin(config()['siteurl'], path)


def social(msg, url):
    """Returns lines for social widgets.

    msg - the message to share.
    url - the url to share.
    """

    # Append a period to the end of the message (if needed)
    if msg[-1] in string.ascii_letters + string.digits:
        msg = msg + '.'


    # Get the configuration
    cfg = config()


    # Create and return the widgets

    template = \
      '  * [<span class="fa fa-%(service)s badge"></span>](%(url)s)'

    twitterdata = {'url':url, 'text':msg}
    if 'twittername' in cfg:
        twitterdata['via'] = '@' + cfg['twittername']
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

    return '<div class="social">',\
      '\n'.join([twitter, facebook, google, linkedin, email]),\
      '</div><!-- class="social" -->'
