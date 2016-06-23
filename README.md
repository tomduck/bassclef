
Bassclef CMS
============

Bassclef is a command-line [CMS] that generates static Web pages from plain old text files.

Features:

  * Content is written [pandoc]-flavoured [markdown], an
    easy-to-read Web writing format;
  * Markdown sources are stored by the user in regular files, 
    and are never databased or otherwise removed from the user's
    control;
  * A templating system is used to define the outer html structure;
  * A command-line front end (`bcms`) manages the processing;
  * The back end uses stable and mature unix tools, including 
    [GNU make], [pandoc] and [ImageMagick] convert;
  * Facilities for constructing blogs and RSS feeds are provided;
  * CSS, font, and social media extras are provided to enable a
    quick start; and
  * A test server is provided to view the generated Web pages.

Bassclef was [inspired] by Tyler Cipriani's "Replacing Jekyll with Pandoc and a Makefile".  It powers the author's [blog].

I am pleased to receive feedback via bassclef's [Issues tracker].

[CMS]: https://en.wikipedia.org/wiki/Content_management_system
[markdown]: https://daringfireball.net/projects/markdown/syntax 
[GNU make]: https://www.gnu.org/software/make/
[pandoc]: http://pandoc.org/
[ImageMagick]: http://imagemagick.org/script/index.php
[inspired]: https://tylercipriani.com/2014/05/13/replace-jekyll-with-pandoc-makefile.html
[blog]: http://tomduck.ca/
[Issues tracker]: https://github.com/tomduck/bassclef/issues


Prerequisites
-------------

Bassclef was written for unix-derived systems such as linux, Mac OS X and CygWin.  The following prerequisites must be installed before proceeding:

  * [GNU make]
  * [Pandoc]
  * [Python 3]
  * [ImageMagick]

[Python 3]: http://python.org/


Installation
------------

To install Bassclef, you should download the source and install it (as root) using:

    $ python3 setup.py install

The installation can be tested using:

    $ bcms test


Quick Start
-----------

To initialize a new bassclef project, `cd` into an empty directory and execute:

    $ bcms init --extras

This installs the build infrastructure in your current directory along with some extras (css, fonts, ...) to enable a quick start.  A sample markdown file is given in the `markdown/` directory.

To build the site, run:

    $ bcms make

Output is written to `www/`.  To view it with a test server, run

    $ bcms serve

and point your browser to `http://127.0.0.1:8000/`.


Details
-------

The following discussion assumes that you are working from the command line and are currently in your bassclef project's root.


### Initialization ###

A project is initialized using:

    $ bcms init

The following visible files and subdirectories are created:

    config.ini css/ fonts/ images/ javascript/ markdown/

The root directory contains a hidden file `.Makefile` and the subdirectories each contain a `.module.mk` file.  These manage the build.

There are two flags that may be used with the `init` command.

  * `--extras`: Populates the directories with css, fonts, etc.
    Also creates and populates the directory `templates`.

  * `--force`: Forces the overwriting of existing files.


### Configuration ###

Site configuration is given in the `config.ini`, which is documented internally.  All configuration items are made available to the bassclef templating system.

You should immediately set the `site-url` field in `config.ini`.


### Markdown ###

Bassclef uses pandoc-flavoured markdown.  A variety of extensions to [standard markdown] are supported.  Please see [Pandoc's Markdown] for the details.

Markdown files should end with a `.md` extension and be saved to the `markdown/` directory.  You may use whatever subdirectory structure you wish.

[standard markdown]: https://daringfireball.net/projects/markdown/syntax 
[Pandoc's Markdown]: http://pandoc.org/README.html#pandocs-markdown


### Metadata ###

[YAML] metadata blocks may be placed at the top of markdown files.  All metadata items are provided to the templating system.  Here is an example metadata block adapted from one of my [articles]:

~~~
---
title: Echoes of Walkerton in Environment Canada cuts
subtitle: Health and safety of Canadians is at risk with latest slashing of Environment Canada budget.
author: Thomas J. Duck
date: 19 March 2014
image: /images/tiles/2014-03-19_thestar.png
caption: As seen in The Toronto Star.
...
~~~

The following metadata fields are recognized by bassclef.  You may define these in `config.ini` or in YAML metadata blocks:

  * All variables in `config.ini`; and
  * `title` - the title for the page;
  * `image` - the relative URL to an image associated with the page.

The following metadata fields are reserved by bassclef.  You may not use these for other purposes:

  * `body` - the html body injected into the template;
  * `web-root` - the Web root for the site;
  * `quoted-title` - the document title with URL-escaped characters;
  * `permalink` - the page's permalink;
  * `quoted-permalink` - the URL-escaped permalink;
  * `composed-page` - presence indicates to the template that a
    composed page is being created.


[YAML]: http://www.yaml.org/
[articles]: http://tomduck.ca/commentary/2014-03-19_echoes-of-walkerton.html


### Images ###

Images should be stored in the `images/` directory.

The image associated with each page should be listed the in the metadata block.  It will normally be inserted between the first and second elements of your content.

URLs for images in your documents should begin with `/images/`.


### Composed pages ###

Composed pages are assembled from the contents of other pages.  An example is a summary page for a series of blog posts.

Composed pages are defined by `.md.in` files and should be stored in the `markdown` directory.  Composed pages contain regular markdown text and filename listings with one filename per line.  Bassclef replaces the filenames with each file's contents.  Here is an example adapted from my [blog]:

~~~
---
title: Latest Posts
...

markdown/posts/2015-09-29_get-science-right.md
markdown/posts/2015-09-28_emissions-targets-compared.md
markdown/posts/2015-09-26_thousands-of-interviews.md
markdown/posts/2015-09-25_list-of-muzzled-scientists.md
markdown/posts/2015-09-22_get-science-right.md
~~~

Often it is undesirable to include the full text for each filename entry.  See [Processing Flags](#processing-flags), below.

[blog]: http://tomduck.ca/


### Processing Flags ###

Processing flags are used in markdown files to fine-tune how content is displayed.  The following flags are supported:

`<!-- image -->`
  ~ Marks where the image defined in the metadata should be inserted.

`<!-- vspace -->`
  ~ Adds some vertical space.

`<!-- break -->`
  ~ Inserts a line break that clears to both margins.

`<!-- cut -->`
  ~ Marks where content should be cut when displayed in a composed
    page.  "Read more..." links are automatically added.


### Building ###

To build your pages, run:

    $ bcms make

This command is simply a wrapper for [GNU make], and any processing flags that you would normally use with `make` can be used here.  For example, to only build the html files use:

    $ bcms make html

Other targets include `images`, `css`, `fonts` and `javascript`.

To force a build use:

    $ bcms make -B

This will be needed if you make a change to a template or `config.ini`.

Html is written to `www/`.

Images are copied to `www/images/originals/`.  Versions with reduced size (as set by `imagegeometry` in `config.ini`) are created using `convert` and stored in `www/images/`.  The smaller versions are automatically linked to their full-size originals in the output html.

CSS files are copied to `www/css/` and fonts are copied to `www/fonts/`.


### Templates ###

Html templates are stored in `templates/`.  You can -- and should -- edit these templates and create new ones.

The template language is pandoc's own, with one exception: An `$include()$` function is provided by [pandoc-tpp].

There is not currently any documentation for the pandoc template language, but it is pretty easily discerned by reading the sources.  Pandoc template directives are enclosed by dollar signs.  Everything else is html.

All configuration and metadata items are provided to the template.

[pandoc-tpp]: https://github.com/tomduck/pandoc-tpp


### Testing ###

To view your pages, use:

    $ bcms serve

and point your browser to `http://127.0.0.1:8000/`.  Type `^C` to exit the test server.


Licenses
--------

Bassclef is free software, released under the [GPL]. © 2015-2016 Thomas J. Duck.

Bassclef is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

There are GPL-compatible and GPL-friendly components used by Bassclef.  These are found in the `bassclef/subrepos/` directory, and are the copyright of their respective authors.

[GPL]: https://www.gnu.org/copyleft/gpl.html
