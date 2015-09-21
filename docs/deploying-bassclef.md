---
title: 6. Deploying Bassclef
showsocial: False 
...

Deploying to GitHub Pages
-------------------------

***NOTE:** This section still needs to be tested.

[GitHub Pages] allow any [GitHub] project to have a Web site.  You could even start a GitHub project just for the Web site.  An example of a bassclef-generated GitHub Pages site is the [bassclef documentation].

***WARNING:** You should not proceed with the following unless you know what you are doing.  The following steps require you to switch branches and delete files.  You should have backups in case something goes wrong.*

First, change into the root of your GitHub project.

~~~ .bash
$ cd path/to/project
~~~

To add GitHub Pages to your project, start a `gh-pages` branch:

~~~ .bash
$ git checkout -b gh-pages
~~~

Next, clear *everything* out of that branch of the repository:

~~~ .bash
$ git rm *
$ git commit -a -m "Emptied the gh-pages branch."
~~~

Copy the site bassclef generated for you into the root of your gh-pages branch and commit the result:

~~~ .bash
$ cp -R path/to/www/* .
$ git add *
$ git commit -a -m "Added gh-pages site."
~~~

Note: The add command above assumes that you have nothing else in your project directory.  You may need to be more careful.

Finally, push your pages to github:

~~~ .bash
$ git push
~~~

Point your browser at <http://username.github.io/repository> to see the result.

[instructions]: https://pages.github.com/


*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *


Deploying to a server
---------------------

One approach to deploying your site to a server is to simply copy across the generated files in `www/`.

However, you may also use git to deploy the site.  This requires some technical know-how, and so I will describe the process in brief.

Create a bare repository on your server for your sources, and install a post-release hook that responds to new tags.  Add the following code to your bassclef `Makefile`:

~~~
~~~

Here is an example post-release hook:

~~~
~~~



*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *


<nav>
[<< Styling Content](styling-content.html) |
[Top](index.html) |
[Licenses >>](licenses.html)
</nav>
