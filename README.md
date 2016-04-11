
--------------------------------------------------------------------

**NOTICE:** I anticipate a release candidate for bassclef 0.1 in the second half of April 2016.  Please feel welcome to [email me] about it.

**What's new?** `setup.py` makes installing bassclef easy.  Windows is now supported via Cygwin.  Template can be set in doc metadata or `config.ini`.  Image folders changed.  See the [User Guide] for more information.

[email me]: mailto:tomduck@tomduck.ca

--------------------------------------------------------------------

 
Bassclef CMS
============

Bassclef is a static Web site generator that processes plain old text files using stable and mature command-line tools.  It is a simple [CMS] for those who need to maintain a high degree of control over their work.

This project was [inspired] by Tyler Cipriani's "Replacing Jekyll with Pandoc and a Makefile".  Content is written in [markdown] and processed using [GNU make], [pandoc], and [python].  Enter `make` on the command line and bassclef builds your site.

Bassclef powers the author's [blog].  It may also be used to generate [GitHub Pages]; bassclef's documentation is one such example.

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


Resources
---------

  * [Repository] - the latest bassclef sources
  * [Issues tracker] - bug reports and feature requests
  * [About Bassclef] - top-level documentation
  * [User Guide] - how to install and use bassclef
  * [Architecture] - a look under the hood
  * [Deployment] - ideas on how to deploy bassclef sites

[Repository]: https://github.com/tomduck/bassclef/
[Issues tracker]: https://github.com/tomduck/bassclef/issues
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

To build the html, open a terminal and `cd` into `bassclef/`.  Run `make`.  The generated html is saved in `bassclef/www/` along with all of the css, images and so on.

To test the results, run `make serve` from the terminal (type `^C` to exit) and point your browser at `http://127.0.0.1:8000/hello.html`.

That's it!


Motivation
----------

Over the years I have built and deployed numerous small Web sites.  Long-term sustainability has proved to be a problem.  The initial ease-of-use of comprehensive CMSes and programming frameworks inevitably gives way to upgrade and migration headaches.  Extracting content that represents many hours of work can be a practical impossibility.

These tools are not without merit.  Comprehensive CMSes and programming frameworks are useful for creating large-scale, dynamic sites.  The vast majority of Web sites don't need -- and would be better off without -- these capabilities.

Bassclef is my effort to build a simple CMS for small-scale, static sites.  I had a look at static site generators like [Jekyll] and [yst], and found that they didn't quite suit my needs.  Jekyll was going to require a lot of time to figure out, an investment that would need repeating after any time away.  I needed something simpler.  Yst, on the other hand, is a template system that does not provide its own css, fonts, social media widgets, etc.  I needed something more.  Bassclef occupies a space in between these two options.

[Jekyll]: https://jekyllrb.com/
[yst]: https://github.com/jgm/yst


Licenses
--------

Bassclef is free software, released under the [GPL]. © 2015-2016 Thomas J. Duck.

Bassclef is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

There are GPL-compatible and GPL-friendly components used by bassclef.  These are loaded into the submodules directory, and are the copyright of their respective authors.

[GPL]: https://www.gnu.org/copyleft/gpl.html
