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
import urllib.parse
import sys
import os
import io
import subprocess
import copy

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
META = {}


def getconfig(key=None):
    """Returns the configuration as a dict.

    key - a single config item to return
    """

    global CONFIG  # pylint: disable=global-statement
    if CONFIG:
        return CONFIG[key] if key else copy.deepcopy(CONFIG)

    # Read the config.ini into a dict, discarding the section info
    config = {}
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    for section in parser.sections():
        config.update({k:v for k, v in parser.items(section)})

    # Add the web root for this site.  e.g., suppose the site-url is
    # https://tomduck.github.io/bassclef/.  The scheme is 'https', the netloc
    # is 'tomduck.github.io' and the web root is 'bassclef'.
    config['web-root'] = urllib.parse.urlparse(config['site-url'])[2]
    if config['web-root'].startswith('/'):
        config['web-root'] = config['web-root'][1:]
    if config['web-root'].endswith('/'):
        config['web-root'] = config['web-root'][:-1]

    # Store the config
    sanitycheck(config)
    CONFIG = config

    # Return the config dict or a value if the key is given
    return config[key] if key else copy.deepcopy(config)


def getmeta(path, key=None):
    """Returns the metadata dict for the file at path.

    key - a single metadata item to return

    This reads the metadata from the file and combines it with the
    defaults in config.ini.
    """

    # If the META has already been calculated then we can return it
    if path in META:
        return META[path][key] if key else META[path]

    # Get defaults from the config
    meta = getconfig()

    # Read metadata from the file
    with open(path) as f:

        # Check for a YAML block at the top of the file
        if f.readline() != '---\n':
            return meta[key] if key else meta

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

    # Add a quoted title
    if 'title' in meta:
        meta['quoted-title'] = \
          urllib.parse.quote(meta['title']).replace('/', '%2F')
        meta['quoted-plus-title'] = \
          urllib.parse.quote_plus(meta['title']).replace('/', '%2F')

    # Get posted-in files and create html
    mdin = [p for p in meta['posted-in'].replace(' ', '').split(',')
            if path in open(p).read()]
    for p in mdin:
        assert os.path.exists(p)
    titles = [getmeta(p)['title'] for p in mdin]
    urls = [p[8:].replace('.md.in', '.html') for p in mdin]
    meta['posted-in'] = posted_in
    meta['posted-in-html'] = \
      ', '.join('<a href="%s">%s</a>'%(urls[i], titles[i])
                for i in range(len(titles)))

    # Store the metadata
    sanitycheck(meta)
    META[path] = meta

    # Return the metadata
    return meta[key] if key else meta


def sanitycheck(data):
    """Checks to see if the config/meta data are sane.  Make minor tweaks
    where necessary."""
    for k, v in data.items():
        data[k] = str(v)
    if 'site-url' in data and data['site-url']:
        if data['site-url'].endswith('/'):  # Remove trailing slash
            data['site-url'] = data['site-url'][:-1]
    if 'template' in data:
        assert os.path.exists(data['template'])
    if 'image' in data:
        assert data['image'].startswith('/') \
               or data['image'].startswith('http://') \
               or data['image'].startswith('https://')
    if 'twitter-name' in data and data['twitter-name']:
        if data['twitter-name'].startswith('@'):  # Remove leading @
            data['twitter-name'] = data['twitter-name'][1:]
    if 'social-profiles' in data and data['social-profiles']:  # Quote urls
        data['social-profiles'] = ', '.join('"' + p.strip('" ') + '"' \
                  for p in data['social-profiles'].split(','))


def writemeta(meta, f=STDOUT, obfuscate=False):
    """Writes the metadata dict as YAML to f.

    obfuscate - indicates that numbered titles should be obfuscated as
                a workaround to a bug in pandoc.
    """

    f.write('---\n')

    for k, v in meta.items():

        if v is None:
            continue

        if obfuscate and k == 'title':
            # Numbered titles get treated like lists by pandoc.  This messes
            # up the html meta fields.  Make a temporary and unobtrusive
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


def permalink(path):
    """Returns the absolute url for given path relative to the Web root."""
    assert path.startswith('/')
    return getconfig('site-url') + path


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


def write(line, f=STDOUT):
    """Writes the line to f.  Does not append a \n to be consistent with
    os.stdout.write()."""
    f.write(line)
    f.flush()


def writelines(lines, f=STDOUT):
    """Writes the lines to f.  Does not append a \n to be consistent with
    os.stdout.writelines()."""
    f.write(''.join(lines))
    f.flush()


def error(msg, errno=1):
    """Prints an error message and exits."""
    writelines(['\n', msg, '\n\nExiting (%d).\n\n'%errno])
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
