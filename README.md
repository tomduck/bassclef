
Bassclef
========

Bassclef uses command-line tools to build static Web pages from plain old text files.  The results are suitable for viewing from either a computer or a mobile.

It's a feather-weight [CMS] for the impatient.  There are no dababases or programming frameworks.  Content is king.

Bassclef was [inspired] by Tyler Cipriani's "Replacing Jekyll with Pandoc and a Makefile".  It was initially developed (and continues) to manage my blog at <http://tomduck.ca/>.


 1. [Workflow](#workflow)
 2. [Prerequisites](#prerequisites) 
 3. [Installation](#installation)
 4. [Writing Content](#writing-content)
 5. [Building and Testing](#building-and-testing)
 6. [Images](#images)
 7. [CSS Styles](#css-styles)
 8. [Deployment](#deployment) 
 9. [Developer Information](#developer-information) 
10. [Licensing](#licensing)


[CMS]: https://en.wikipedia.org/wiki/Content_management_system

[inspired]: https://tylercipriani.com/2014/05/13/replace-jekyll-with-pandoc-makefile.html


Workflow
--------

A bassclef session proceeds as follows.

All work is done in `bassclef` directory.  Commands are executed in the `bash` shell.

To generate `www/index.html`, open `content/index.md` in a text editor.  Content is written in [markdown]; for example:

    Hello, world!
    =============

    This is a test.

To build the site:

    $ make

To run the test server:

    $ make serve

(type `^C` to exit).  The test site can be viewed at <http://127.0.0.1:8000/>.

When ready, the site can be deployed to your server or via [GitHub] pages.

That's it!

[markdown]: https://daringfireball.net/projects/markdown/syntax
[GitHub]: https://github.com/


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

[Git]: https://git-scm.com/
[Pandoc]: http://pandoc.org/README.html
[Pandoc User Guide]: http://pandoc.org/README.html
[GNU make]: https://www.gnu.org/software/make/
[Python]: http://python.org/
[pyyaml]: http://pyyaml.org/
[ImageMagick]: http://imagemagick.org/script/index.php


Installation
------------

Installation requires the following steps:

 1) Clone bassclef's git repository with the `--recursive` flag:

    $ git clone https://github.com/tomduck/bassclef.git --recursive

Change into your installation directory:

    $ cd bassclef


 2) Execute `make && make serve` and point your browser at
<http://127.0.0.1:8000/> to test your installation.  You should
see a page claiming "Success!".

If the install wasn't successful, check the error message from
the build process.  You may need to:

  * Install a prerequisite that you are missing;
  * install Python 3 (python 2 is not enough);
  * install PyYAML into Python 3 (use `pip3` for this).

If you experience other troubles, please file an Issue at the
bassclef GitHub [repository](http://github.com/tomduck/bassclef).


 3) Create a new branch for your content:

    $ git checkout -b <branchname>

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
  * date - in whatever format
  * updated - date, in whatever format
  * publisher - name of the original publisher of the content 
  * source - url for the original publication of the content 
  * image - URL for an image file
  * caption - caption for the image

and

  * showtitle - flags that title block should be shown (default
    True)
  * showsocial - flags that social buttons should be shown (default
    True) 

There are no required metadata.

You may also define your own metadata fields.  Note, however, that all names in the config.ini are reserved, as are the following:

  * titleclass
  * permalink


### Markdown ###

Content is written in [Pandoc-flavoured markdown][Pandoc Users Guide].  Markdown is a plain-text Web writing format.  Writing markdown content is much like writing an email.


### Images ###

The metadata image will be inserted between the first and second elements of your content.  It is also used to construct tags for Facebook, Google Plus and Twitter.  For better control, mark where the image should be inserted using a `<!-- image -->` tag (on its own line).


### Composed pages ###

Bassclef supports the generation of composed pages via `.md.in` files.  Such files are used to create temporary `.md` files from which `.html` files are generated).  This functionality is needed to generate blog pages.

The composed page should consist of ordinary markdown and filename lines.  If the filenames refer to `.md` content files, then they are read, processed and inserted; otherwise they are printed out as-is.

Normally the entire content of the referenced file is inserted.  You can use `<!-- break -->` in the inserting file to indicate that any remaining content be truncated.  "Read more..." links are automatically added to the composed page.


Building and Testing
--------------------

To build your site run

    $ make

All files are written to the `www/` folder.

To test your site run

    $ make serve

If you are confident the build will succeed, use

    $ make && make serve

instead.


Images
------

High-resolution images should be stored in the `images/` folder.  These images are copied to `www/images` during the build process.  Large thumbnails are generated and stored in `www/images/thumbs/`.  You should link to the thumbs from your content.

SVG images are handled separately because of the vector format.  They should be placed in `images/svg/`.  The build process writes png versions into the `www/images/thumbs/` and `www/images/icons/` directories.


CSS Styles
----------

[Skeleton] provides a foundation of responsive css that allows bassclef sites to be viewed on either a computer or a mobile.  Custom css for bassclef is provided by `css/bassclef.css`.

Knowledge of css is required to give your site its own look-and-feel.  If you want to adjust the css, you may either edit `css/bassclef.css` or create a new `css/custom.css` and patch it into the Makefile.

[Skeleton]: http://getskeleton.com/


Deployment
----------

TO BE WRITTEN.


Developer Information
---------------------

Below is more advanced information for developers.  Most users will not require this information.


### HTML Templates ###

Bassclef's pandoc html template is given in `templates/default.html5`.  If you want to edit it, read about [pandoc templates] first.  All bassclef metadata and config.ini fields are available to the template.

[pandoc templates]: http://pandoc.org/README.html#templates


### Scripts ###

There are three python scripts used in the build process:

  * `scripts/compose.py`: Processes all `.md.in` files;
  * `scripts/preprocess.py`: Preprocesses all `.md` files; and
  * `scripts/postprocess.py`: Postprocesses all pandoc output.

There is also `scripts/util.py` which provides common code for the three scripts.

One important thing the scripts do is inject social widgets.  So, code for the widgets is found in `scripts/util.py` and not `templates/default.html5` as you might expect.


### Fonts ###

Bassclef uses [Open Sans] for its font.  For privacy reasons this is aggregated with bassclef rather than linking to google Web fonts.  There is no need to expose users to unnecessary tracking

[Font Awesome] is used for the social widgets.

[Open Sans]: https://www.google.com/fonts/specimen/Open+Sans
[Font Awesome]: http://fontawesome.io/


Licensing
---------

Bassclef source files are licensed under the GNU General Public License (GPL), version 3.

There are GPL-compatible and GPL-friendly packages aggregated with Bassclef.  These are found in the submodules directory, and are automatically retrieved from separate repositories when you install Bassclef.
