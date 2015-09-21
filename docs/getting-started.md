---
title: Getting Started
showsocial: False 
...


Prerequisites
-------------

Before proceeding, you will need to install the tools that bassclef needs.  The first two provide the foundation:

  * [Pandoc] is used to generate html from markdown content.

  * [GNU make] manages the build.  Make normally comes pre-installed
    on unix-like systems (e.g., linux and Mac OS X).  We will use
    simple commands like `make` and `make serve`.

The next three prerequisites operate entirely behind-the-scenes:

  * [Python] 3 is used for bassclef's preprocessing and
    postprocessing scripts.  You *must* have version 3.x; python 2.x
    will not suffice.

  * [PyYAML], a third-party python module, is used for metadata
    parsing.  The usual command to download and install it (as root)
    is `pip3 install pyyaml`.  You may get a message saying "fatal
    error: 'yaml.h' file not found".  Ignore it.  The complaint is
    due to an optional library that can't be found.

  * [ImageMagick] convert for image processing.

The following optional packages may also be helpful:

  * [Git] may be used to manage your bassclef sources and content. 
    It is required if you want to *install* your generated site into
    [GitHub Pages].

[Pandoc]: http://pandoc.org/README.html
[GNU make]: https://www.gnu.org/software/make/
[Python]: http://python.org/
[PyYAML]: http://pyyaml.org/
[ImageMagick]: http://imagemagick.org/script/index.php
[Git]: https://git-scm.com/
[GitHub Pages]: https://pages.github.com/


*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *


Installing bassclef
-------------------

To install bassclef take the following steps:

 1) Download the bassclef sources.  You may either 
    [download the zip] or clone the sources using git.

    Cloning bassclef's git repository must be done with the
    `--recursive` flag:
    
    ~~~ .bash
    $ git clone https://github.com/tomduck/bassclef.git --recursive
    ~~~

    Before continuing further, change into your installation
    directory:

    ~~~ .bash
    $ cd bassclef


 2) To test your installation, execute `make && make serve` and
    point your browser at <http://127.0.0.1:8000/>.  You should
    see a page claiming "Success!".

    If the install wasn't successful, check the error message from
    the build process.  You may need to:

      * Install a prerequisite that you are missing;
      * install python 3 (python 2 is not enough); or
      * install PyYAML into Python 3 (use `pip3`, not `pip`, for
        this).

    If you experience other any troubles, please file an Issue at the
    [bassclef repository] on [GitHub].


 3) Build the documentation by executing

    ~~~ .bash
    $ make docs
    ~~~

    Execute `make serve` like before and point your browser at
    <http://127.0.0.1:8000/docs/index.html> to read the
    docs.  You may also wish to view the sources in the `docs/`
    directory.


 4) Configure bassclef by editing the `config.ini`.

    Note: If you cloned the repository the you may wish to
    create a new branch for your changes:

    ~~~ .bash
    $ git checkout -b <branchname>
    ~~~

    (replace `<branchname>` with the name you have chosen).

[download the zip]: https://github.com/tomduck/bassclef/archive/master.zip
[bassclef repository]: http://github.com/tomduck/bassclef
[GitHub]: https://github.com/


*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *


<nav>
[<< Example Session](example-session.html) |
[Top](/docs/index.html) |
[Writing Content >>](writing-content.html)
</nav>
