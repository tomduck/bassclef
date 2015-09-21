---
title: Example Session
showsocial: False
...

Here is a quick example of the basic workflow to whet your appetite.  We begin by creating some content using a text editor. For example:

```
Hello, world!
=============

This is a test.
```

Let's save this to `content/index.md`.  Content is written in [markdown], an easy-to-read Web writing format.  More on that later.

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

<nav>
[Top](/docs/index.html) | 
[Getting started >>](/docs/getting-started.html)
</nav>
