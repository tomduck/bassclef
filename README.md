
Bassclef
========

Bassclef uses command-line tools to build static Web pages from plain old text files.  The results are suitable for viewing from either a computer or a mobile.

It's a feather-weight [CMS] for the impatient.  There are no dababases or programming frameworks.  Content is king.

Bassclef was [inspired] by Tyler Cipriani's "Replacing Jekyll with Pandoc and a Makefile".  It was initially developed (and continues) to manage my blog at <http://tomduck.ca/>.


 1. [Workflow](#workflow)
 2. [Technologies](#technologies) 
 3. [Prerequisites](#prerequisites) 
 4. [Installation](#installation)
 5. [Writing Content](#writing-content)
 6. [Deployment](#deployment)
 7. [Licensing](#licensing)


[CMS]: https://en.wikipedia.org/wiki/Content_management_system

[inspiration]: https://tylercipriani.com/2014/05/13/replace-jekyll-with-pandoc-makefile.html


Workflow
--------

A bassclef session proceeds as follows.

All work is done in `bassclef` directory.  Commands are executed in the `bash` shell.

To generate `www/index.html`, open `content/index.md` in a text editor.  Content is written in [markdown]; for example:

~~~
Hello, world!
=============

This is a test.
~~~

To build the site:

~~~ .bash
$ make
~~~

To run the test server:

~~~ .bash
$ make serve
~~~

(type `^C` to exit).  The test site can be viewed at <http://127.0.0.1:8000/>.

When ready, the site can be deployed to your server or via [GitHub] pages.

That's it!


Prerequisites
-------------

The following prerequisites must be installed before proceeding:

  * [Git] to manage the bassclef sources and your content.  Some
    familiarity with git (or version control systems in general) is
    needed.

  * [Pandoc] for html generation from markdown content.  Read the
    [Pandoc User Guide] for extensions to standard markdown.

  * [GNU make] to manage the build.  Make normally comes
    pre-installed on unix-like systems (e.g., linux and Mac OS X). 

  * [Python] 3 with for bassclef's preprocessing and postprocessing
    scripts.  Python 2 will not suffice.

  * [PyYAML], a module for Python 3.  The usual command (as root) to
    download and install it is `pip3 install pyyaml`.

  * [ImageMagick] convert for image processing.


Installation
------------

Installation requires the following steps:

 1) Clone baseclef's git repository with the `--recursive` flag:

    ~~~ .bash
    $ git clone https://github.com/tomduck/baseclef.git --recursive
    ~~~~

    Change into your installation directory:

    ~~~ .bash
    $ cd bassclef
    ~~~~


 2) Execute `make && make serve` and point your browser at
    <http://127.0.0.1:8000/> to test your installation.  You should see a
    page claiming "Success!".

    If the install wasn't successful, check the error message from
    the build process.  You may need to:

      * Install a prerequisite that you are missing;
      * install Python 3 (python 2 is not enough);
      * install PyYAML into Python 3 (use `pip3` for this).

    If you experience other troubles, please file an Issue at the
    bassclef GitHub [repository](http://github.com/tomduck/bassclef).


 3) Create a new branch for your content:

    ~~~ .bash
    $ git checkout -b <branchname>
    ~~~
    (replace `<branchname>` with the name you have chosen.  You are
    now ready to begin building content.

 4) Edit the `config.ini` file to provide the basic configuration. 


Writing Content
---------------

Markdown text files go in the `content` directory.  You may use whatever directory structure you wish.  The only requirement is that the files have `.md` extensions.  The `.md` files are used to generate `.html` files with the same filename and in the same directory structure.  Processing is guided by the config.ini and metadata blocks in your documents.


### Metadata ###

A metadata block may be placed at the top of a markdown file.  It should be bounded by a `---` at the top and a `...` at the bottom.

Metadata fields recognized by bassclef include

  * title, subtitle
  * description - a description of the content, 155 characters max
  * date - the publication date, in whatever format
  * publisher - name of the original publisher of the content 
  * source - url for the original publication of the content 
  * social - flags if social buttons should be shown (default True) 
  * image - URL for an image file
  * caption - caption for the image

There are no required metadata.

You may also define your own metadata fields.  Note, however, that all names in the config.ini are reserved, as are the following:

  * titleattrs
  * permalink


### Markdown ###

Content is written in [Pandoc-flavoured markdown][Pandoc Users Guide].  Markdown is a plain-text Web writing format.  Writing markdown content is much like writing an email.


### Images ###

The metadata image will be inserted between the first and second elements of your content.  It is also used to construct tags for Facebook, Google Plus and Twitter.  For better control, mark where the image should be inserted using a `<!-- image -->` tag (on its own line).


### Composed pages ###

Bassclef supports the generation of composed pages via `.md.in` files.  This file is used to generate a `.md` file (from which a `.html` file will be created).

The composed page consists of ordinary markdown and filenames.  If the filenames refer to `.md` content files, then they are read, processed and inserted; otherwise they are printed out as-is.



### Reserved names ###




Styling Content
---------------


Deployment
----------

Licensing
---------

Bassclef source files are licensed under the GNU General Public License (GPL), version 3.

There are GPL-compatible and GPL-friendly packages aggregated with Bassclef.  These are found in the submodules directory, and are automatically retrieved from separate repositories when you install Bassclef.



[markdown]: https://daringfireball.net/projects/markdown/syntax
[Pandoc]: http://pandoc.org/README.html
[Pandoc User Guide]: http://pandoc.org/README.html
[Python]: http://python.org/
[pyyaml]: http://pyyaml.org/
[GNU make]: https://www.gnu.org/software/make/
[Skeleton]: http://getskeleton.com/
[Open Sans]: https://www.google.com/fonts/specimen/Open+Sans
[Font Awesome]: http://fontawesome.io/
[Git]: https://git-scm.com/
[GitHub]: https://github.com/
[ImageMagick]:



  * [Skeleton] for responsive css.  Knowledge of css is required to
    give your site its own look-and-feel.

  * [Open Sans] as the font.  This is provided with Bassclef.

  * [Font Awesome] for social widgets.

  * [Git] 
