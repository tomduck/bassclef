---
title: Bassclef
subtitle: The featherweight command-line CMS for the impatient.
image: /images/sized/bassclef2.png
showsocial: False
...

Bassclef builds static Web pages from plain old text files using command-line tools.  The results are suitable for viewing from either a computer or a mobile.

It's a featherweight [CMS] for the impatient.  There are no dababases or programming frameworks.  Content is king.

Bassclef was [inspired] by Tyler Cipriani's "Replacing Jekyll with Pandoc and a Makefile", and can be used to generate [GitHub Pages] for your [GitHub] project.  It was initially developed (and continues) to manage my blog at <http://tomduck.ca/>.

[CMS]: https://en.wikipedia.org/wiki/Content_management_system
[inspired]: https://tylercipriani.com/2014/05/13/replace-jekyll-with-pandoc-makefile.html
[GitHub Pages]: https://pages.github.com/
[GitHub]: https://github.com/


### Contents ###

...


Workflow
--------

The basic workflow for bassclef is straight-forward.  We begin by creating some content using a text editor. For example:

```
Hello, world!
=============

This is a test.
```

Let's save this to `index.md`.  Content is written in [markdown], an easy-to-read Web writing format.  More on that later.

To build the html, open a terminal and change to the `bassclef` install directory. Execute the following at the bash prompt (`$`):

~~~
$ make
~~~

An `index.html` is generated.

To run the test server, execute

```
$ make serve
```

(type `^C` to exit).  The site is viewed at <http://127.0.0.1:8000/>.

That's it!

[markdown]: https://daringfireball.net/projects/markdown/syntax 


*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *

<nav>
Top | [Getting started >>](/doc/getting-started.html)
</nav>
