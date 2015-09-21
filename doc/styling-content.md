---
title: Styling Content
showsocial: False 
...

CSS Styles
----------

[Skeleton] provides a foundation of responsive css that allows bassclef sites to be viewed on either a computer or a mobile.  Custom css for bassclef is provided by `css/bassclef.css`.

Knowledge of css is required to give your site its own look-and-feel.  If you want to adjust the css, you may either edit `css/bassclef.css` or create a new `css/custom.css` and patch it into the Makefile.

[Skeleton]: http://getskeleton.com/


HTML Templates
--------------

Bassclef's pandoc html template is given in `templates/default.html5`.  If you want to edit it, read about [pandoc templates] first.  All bassclef metadata and config.ini fields are available to the template.

[pandoc templates]: http://pandoc.org/README.html#templates


Scripts
-------

There are three python scripts used in the build process:

  * `scripts/compose.py`: Processes all `.md.in` files;
  * `scripts/preprocess.py`: Preprocesses all `.md` files; and
  * `scripts/postprocess.py`: Postprocesses all pandoc output.

There is also `scripts/util.py` which provides common code for the three scripts.

One important thing the scripts do is inject social widgets.  So, code for the widgets is found in `scripts/util.py` and not `templates/default.html5` as you might expect.


Fonts
-----

Bassclef uses [Open Sans] for its font.  For privacy reasons this is aggregated with bassclef rather than linking to google Web fonts.  There is no need to expose users to unnecessary tracking

[Font Awesome] is used for the social widgets.
[Open Sans]: https://www.google.com/fonts/specimen/Open+Sans
[Font Awesome]: http://fontawesome.io/


*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *


<nav>
[<< Building and Testing](/doc/building-and-testing.html) |
[Top](/doc/index.html) |
[Deploying Bassclef >>](/doc/deploying-bassclef.html)
</nav>
