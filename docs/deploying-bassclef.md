---
title: 6. Deploying a Bassclef Site
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

However, you may also use git to deploy the site.  By implementing the following steps you will be able to deploy by executing a simple `make deploy`.

 1. Create a bare repository on your server for your sources on the
    server:

    ~~~ .bash
    $ git init --bare
    ~~~

    Set the bare repository as the remote origin for your local
    repository.  Push to the bare repository.

 2. On your server, clone a copy of the repository as follows:

    ~~~ .bash
    $    $ git clone /path/to/bare/repo /path/to/clone
    ~~~

    Notice that I didn't use `--recursive` to load the submodules. 
    This is because you first need to **edit the .gitmodules file
    and change all the urls to absolute paths**.  Once that
    is done, `cd` into your clone and load the submodules using:

    ~~~ .bash
    $ git submodule init
    $ git submodule update
    ~~~

 3. Install a post-release hook in the bare repository that responds
    to new tags.  The idea here is to perform a new build any time
    the repo sees a new tag.

    Here is a post-release hook that does the job:

    ~~~ .bash
    #! /bin/bash

    # This post-receive hook installs the Web site whenever
    # something is tagged.

    REPO=/path/to/bare/repo
    WORK=/path/to/local/repo

    # Check that the working repository exists
    if [ ! -d $WORK ]; then \
        echo "ERROR: Working repository does not exist."; \
        exit 1;
    fi

    process_ref() {

        # Parse the REF
        oldrev=$(git rev-parse $1)
        newrev=$(git rev-parse $2)
        refname="$3"

        # Get the rev type using git-cat-file
        rev_type=$(git cat-file -t $newrev 2> /dev/null)

        case "$refname","$rev_type" in
          refs/tags/*,tag)
            # Install by doing a checkout
            echo "Post-receive hook initiating install..."
            cd $WORK \
            && GIT_DIR=$REPO GIT_WORK_TREE=$WORK git checkout -f \
            && GIT_DIR=$REPO GIT_WORK_TREE=$WORK git submodule update \
          	&& GIT_DIR=$REPO GIT_WORK_TREE=$WORK \
                   git submodule foreach git checkout -f \
            && make \
            && echo "Done."
          ;;
        esac
    }

    # Process each line of stdin
    while read REF; do process_ref $REF; done
    ~~~

 4. Configure your Web server to serve files from the `www/`
    directory of your clone.

 5. Add the following code to the bassclef `Makefile` on your local
    machine.  It will automatically tag and push when you execute
   `make deploy`:

    ~~~
    # Use the current date as the install tag
    TAG = $(shell date "+%Y-%m-%d")

    # Flag if the tag exists
    TAGEXISTS = $(shell GIT_DIR=.git git rev-parse $(TAG) >/dev/null 2>&1; echo $$?)

    # A post-receive hook does the install in response to a tag
    ifeq ($(TAGEXISTS),0)
    deploy:
    	git push --recurse-submodules=on-demand
    	git tag -d $(TAG)
    	git push origin :refs/tags/$(TAG)
    	git tag -a $(TAG) -m "Install tag for $(TAG)."
    	git push origin $(TAG)
    else
    deploy:
    	git push --recurse-submodules=on-demand
    	git tag -a $(TAG) -m "Install tag for $(TAG)."
    	git push origin $(TAG)
    endif
    ~~~


*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *


<nav>
[<< Styling Content](styling-content.html) |
[Top](index.html) |
[Licenses >>](licenses.html)
</nav>
