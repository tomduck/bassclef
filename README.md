
`bassclef`: A simple command-line CMS for the impatient
======================================================= 

`bassclef` is a content management system (CMS) for building static Web pages and blog sites.  It employs widely-available command-line tools to generate html pages from plain old text files.  It's dead-simple to use.  For an example of `bassclef` in action, see <http://tomduck.ca/>.

The [inspiration] for `bassclef` was Tyler Cipriani's "Replacing Jekyll with Pandoc and a Makefile".


 1. [Technologies](#technologies) 
 2. [Prerequisites](#prerequisites) 
 3. [Installation](#installation)
 4. [Licensing](#licensing)


TO DO: Write user documentation.


Technologies
------------

`bassclef` leverages the following existing technologies:

  * `pandoc` for html generation from markdown content;
  * `python` scripts for preprocessing and postprocessing;
  * GNU `make` to manage the build;
  * Skeleton for responsive css;
  * Open Sans as the font;
  * Font Awesome for social widgets; and
  * `git` to manage content and site deployment.

You won't have to worry about most of this.  Your job is to build content!


Prerequisites
-------------

The following prerequisites must be installed before proceeding:

  * git 
  * GNU make
  * pandoc
  * python 3 with the `pyyaml` package


Installation
------------

To install, simply clone `baseclef`'s git repository.  Enter the `bassclef` directory and execute the following at the `bash` prompt:

    $ make && make serve

Point your browser at <http://127.0.0.1/>.  You should see a page claiming "Success!".


Licensing
---------

`bassclef` source files are licensed under the GNU General Public License (GPL), version 3.

There are GPL-compatible and GPL-friendly packages aggregated with `bassclef`.  These are found in the submodules directory, and are automatically retrieved from separately-maintained repositories when you install `baseclef`.