---
title: 1. Example Session
showsocial: False
...

Here is a quick example of the workflow to whet your appetite.  We begin by creating some content using a text editor. Suppose we save the following to `content/index.md`:

~~~
Hello, world!
=============

It's a bright sunshiny day.
~~~

Content is written in [markdown], an easy-to-read Web writing format.  More on that later.

To build the html, we open a terminal and `cd` into the `bassclef` install directory, then run `make` at the bash prompt (`$`):

~~~ .bash
$ make
~~~

An `index.html` is generated.

To test our results, we execute

~~~ .bash
$ make serve
~~~

(type `^C` to exit), and point our browser to <http://127.0.0.1:8000/>.

That's it!

[markdown]: https://daringfireball.net/projects/markdown/syntax 


*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *


<nav>
[Top](index.html) | 
[Getting started >>](getting-started.html)
</nav>
