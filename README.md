
Bassclef
========

Bassclef is a static Web site generator that processes plain old text files using stable and mature command-line tools.  It is a simple [CMS] for those who need to maintain a high level of control over their work.  Content is written in [markdown] and is processed behind the scenes using [GNU make], [pandoc], [python], and [ImageMagick] convert.

This project was [inspired] by Tyler Cipriani's "Replacing Jekyll with Pandoc and a Makefile".  It was written as a way to escape the long-term maintenance challenges associated with databasing CMSes and Web programming frameworks.

Bassclef powers the author's blog at <http://tomduck.ca/>.  It may also be used to generate [GitHub Pages]; bassclef's documentation is one such example.

Sources and an issue tracker can be found at the [bassclef repository page] on github.

[markdown]: https://daringfireball.net/projects/markdown/syntax 
[GNU make]: https://www.gnu.org/software/make/
[pandoc]: http://pandoc.org/
[python]: http://python.org/
[ImageMagick]: http://imagemagick.org/script/index.php
[CMS]: https://en.wikipedia.org/wiki/Content_management_system
[inspired]: https://tylercipriani.com/2014/05/13/replace-jekyll-with-pandoc-makefile.html
[GitHub Pages]: https://pages.github.com/
[bassclef repository page]: https://github.com/tomduck/bassclef/


Documentation
-------------

  * [User Guide] - explains how to install and use bassclef
  * [Architecture] - explains what bassclef is doing under the hood
  * [Deploying Bassclef] - some ideas on how you can deploy
    bassclef-generated sites

[User Guide]: https://tomduck.github.io/bassclef/bassclef-user-guide.html
[Architecture]: https://tomduck.github.io/bassclef/bassclef-architecture.html
[Deploying Bassclef]: https://tomduck.github.io/bassclef/deploying-bassclef.html


Workflow Example
----------------

Suppose we save the following to `bassclef/markdown/hello.md`:

~~~
Hello, world!
=============

It's a bright sunshiny day.
~~~

Name your `.md` files however you like.  Bassclef will find them so long as they have a `.md` extension and are in `bassclef/markdown/` or one of its subdirectories.

To build the html, open a terminal and `cd` into `bassclef/`.  Run `make`.  The generated html is saved in `bassclef/www/` along with all of the css, images and so on.

To test the results, run `make serve` from the terminal (type `^C` to exit) and point your browser at <http://127.0.0.1:8000/hello.html>.


Rationale
---------

Over the years I have built and deployed numerous small-scale Web sites.  Long-term maintenance has proved to be a recurring problem.  The initial easy-of-use of comprehensive CMSes and programming frameworks inevitably gives way to upgrade and migration headaches.  Content representing many hours of work is consumed and stored in relational databases.  Getting that content out can be practically impossible.

These tools are not without merit.  Comprehensive CMSes and programming frameworks are useful for creating large-scale, dynamic sites.  However, the vast majority of Web sites don't need (and would be better off without) these capabilities.

Bassclef is my effort to build a simple CMS for small-scale, static Web sites.  Content is stored as plain text in directories.  Familiar, mature and stable tools are used behind the scenes.  Modern necessities (e.g., social media support) are included, but in a way that doesn't compromise the privacy of Web site visitors.  A variety of niceties that simplify the task of creating a site are provided by python scripts.


Licenses
--------

Bassclef is free software, released under the [GPL]. © 2015-2016 Thomas J. Duck.

There are GPL-compatible and GPL-friendly components aggregated with Bassclef.  These are found in the submodules directory, and are the copyright of their respective authors.

[GPL]: https://www.gnu.org/copyleft/gpl.html
