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

"""util.py - utility functions for bassclef."""

import configparser
import re
from urllib.parse import urlparse, quote
import sys
import os
import io
import subprocess

import yaml


# Py3 strings are unicode: https://docs.python.org/3.5/howto/unicode.html.
# Character encoding/decoding is performed automatically at stream
# interfaces: https://stackoverflow.com/questions/16549332/.
# Set it to UTF-8 for all streams.
STDIN = io.TextIOWrapper(sys.stdin.buffer, 'utf-8', 'strict')
STDOUT = io.TextIOWrapper(sys.stdout.buffer, 'utf-8', 'strict')
STDERR = io.TextIOWrapper(sys.stderr.buffer, 'utf-8', 'strict')

# Global data stores.  These data should not change in a single execution.
CONFIG = None
META = None


def defaults(config):
    """Returns a dict of config defaults."""
    return {'site-url':'',
            'template':'',
            'image-geometry':'250x500',
            'schema-name':'',
            'schema-type':'',
            'schema-url':'',
            'email':'',
            'twitter-name':'',
            'social-profiles':''}


def getconfig(key=None):
    """Returns the configuration as a dict.

    key - a single config item to return
    """

    global CONFIG  # pylint: disable=global-statement
    if not CONFIG is None:
        return CONFIG[key] if key else CONFIG

    # Read the config.ini into a dict, discarding the section info
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    config = defaults({})
    for section in parser.sections():
        config.update({k:v for k, v in parser.items(section)})

    # Add the domain name and web root for this site so that they may be used
    # by the template.  e.g., suppose the site-url is
    # https://tomduck.github.io/bassclef/.  The domain name is
    # tomduck.github.io and the web root is /bassclef.
    config['domain-name'] = urlparse(config['site-url'])[1]
    config['web-root'] = urlparse(config['site-url'])[2]
    if config['web-root'].endswith('/'):
        config['web-root'] = config['web-root'][:-1]

    # Store the config
    sanitycheck(config)
    CONFIG = config

    # Return the config dict or a value if the key is given
    return config[key] if key else config


def getmeta(path, key=None):
    """Returns the metadata dict for the file at path.

    key - a single metadata item to return

    This reads the metadata from the file and combines it with the
    defaults in config.ini.
    """

    # If the META has already been calculated then we can return it
    global META  # pylint: disable=global-statement
    if not META is None:
        return META[key] if key else META

    # Get defaults from the config
    meta = getconfig()

    # Read metadata from the file
    with open(path) as f:

        # Check for a YAML block at the top of the file
        if f.readline() != '---\n':
            return meta

        # Read in the metadata block
        lines = ['---']
        for line in f:
            lines.append(line)
            if line == '...\n':  # Signifies end of the metadata block
                break

    # Confirm the end of the metadata block was found
    if lines[-1] != '...\n':
        raise RuntimeError('End of YAML metadata block not found.')

    # Parse the metadata
    meta.update(yaml.load('\n'.join(lines)))

    # Add an encoded title
    meta['encoded-title'] = quote(meta['title']).replace('/', '%2F')

    # Store the metadata
    sanitycheck(meta)
    META = meta

    # Return the metadata
    return meta[key] if key else meta


def sanitycheck(data):
    """Checks to see if the config/meta data are sane.  Make minor tweaks
    where necessary."""
    if 'template' in data:
        assert os.path.exists(data['template'])
    if 'image' in data:
        assert data['image'].startswith('/') \
               or data['image'].startswith('http://') \
               or data['image'].startswith('https://')
    if 'twitter-name' in data:
        if data['twitter-name'].startswith('@'):  # Remove leading @
            data['twitter-name'] = data['twitter-name'][1:]
    if 'social-profiles' in data:  # Quote urls
        data['social-profiles'] = ', '.join('"' + p.strip('" ') + '"' \
                  for p in data['social-profiles'].split(','))


def printmeta(meta, f=STDOUT, obfuscate=False):
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
    f.flush()


def getcontent(path):
    """Returns the content of a .md file as a list of lines."""

    with open(path) as f:

        # Skip the metadata
        if f.readline() == '---\n':
            while f.readline() != '...\n':
                continue
        else:
            f.seek(0)

        # Return the content
        return [line for line in f]


def printline(line, f=STDOUT):
    """Prints the line to f."""
    f.write(line)
    f.flush()


def printlines(lines, f=STDOUT):
    """Prints the lines to f."""
    f.write(''.join(lines))
    f.flush()


def error(msg, errno=1):
    """Prints an error message and exits."""
    printlines(['\n', msg, '\n\nExiting (%d).\n\n'%errno])
    sys.exit(errno)


def which(name):
    """Locates a program name on the user's path."""
    # Don't use shutil.which() here.  Shell out so that we see the same
    # thing as the GNU make.  This is essential for cygwin installs.
    try:
        output = subprocess.check_output(['which', name])
        return output.decode(encoding='UTF-8').strip()
    except subprocess.CalledProcessError:
        return None
