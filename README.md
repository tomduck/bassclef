
--------------------------------------------------------------------

<!-- image -->

**NOTICE:** This software is not officially released.  Although it is being used in production, the software is developing rapidly.

What's new?

A `setup.py` script makes installing bassclef much easier.  See the [User Guide].

<!-- break -->

--------------------------------------------------------------------

 
Bassclef CMS
============

Bassclef is a static Web site generator that processes plain old text files using stable and mature command-line tools.  It is a simple [CMS] for those who want a high degree of control over their work.

This project was [inspired] by Tyler Cipriani's "Replacing Jekyll with Pandoc and a Makefile".  Content is written in [markdown] and is processed using [GNU make], [pandoc], [python], and [ImageMagick] convert.

Bassclef powers the author's [blog].  It may also be used to generate [GitHub Pages]; bassclef's documentation is one such example.

Sources and an issue tracker can be found at the [bassclef repository page] on GitHub.

[markdown]: https://daringfireball.net/projects/markdown/syntax 
[GNU make]: https://www.gnu.org/software/make/
[pandoc]: http://pandoc.org/
[python]: http://python.org/
[ImageMagick]: http://imagemagick.org/script/index.php
[CMS]: https://en.wikipedia.org/wiki/Content_management_system
[inspired]: https://tylercipriani.com/2014/05/13/replace-jekyll-with-pandoc-makefile.html
[blog]: http://tomduck.ca/
[GitHub Pages]: https://pages.github.com/
[bassclef repository page]: https://github.com/tomduck/bassclef/


Documentation
-------------

  * [User Guide] - explains how to install and use bassclef
  * [Architecture] - explains what bassclef is doing under the hood
  * [Deployment] - some ideas on how you can deploy
    bassclef-generated sites

[About Bassclef]: https://tomduck.github.io/bassclef/
[User Guide]: https://tomduck.github.io/bassclef/bassclef-user-guide.html
[Architecture]: https://tomduck.github.io/bassclef/bassclef-architecture.html
[Deployment]: https://tomduck.github.io/bassclef/deploying-bassclef.html


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

To test the results, run `make serve` from the terminal (type `^C` to exit) and point your browser at http://127.0.0.1:8000/hello.html.


Rationale
---------

Over the years I have built and deployed numerous small-scale Web sites.  Long-term maintenance has proved to be a recurring problem.  The initial easy-of-use of comprehensive CMSes and programming frameworks inevitably gives way to upgrade and migration headaches.  Extracting content that represents many hours of work can be a practical impossibility.

These tools are not without merit.  Comprehensive CMSes and programming frameworks are useful for creating large-scale, dynamic sites.  The vast majority of Web sites don't need -- and would be better off without -- these capabilities.

Bassclef is my effort to build a simple CMS for small-scale, static Web sites.  It is easy to get started with: Simply throw some content into `bassclef/markdown/` and you are on your way.  Familiar, mature and stable tools are used to process it, and additional niceties are provided by python scripts.  A foundation of responsive css ensures that your site looks good right out of the box on screens large and small.  Ultimately, you can focus on what matters most: generating content.


Licenses
--------

Bassclef is free software, released under the [GPL]. © 2015-2016 Thomas J. Duck.

There are GPL-compatible and GPL-friendly components used by Bassclef.  These are loaded into the submodules directory, and are the copyright of their respective authors.

[GPL]: https://www.gnu.org/copyleft/gpl.html
