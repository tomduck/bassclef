---
title: Writing Content
showsocial: False 
...

Markdown documents
------------------

All content is written in [markdown], an easy-to-read Web writing format.  If you are not familiar with markdown, check out GitHub's [Markdown Basics].  Bassclef's markdown processor supports a number of extensions to standard markdown; please see the [Pandoc User Guide].

Markdown text files should be put in the `content` directory.  You may use whatever subdirectory structure you wish.  You can also choose whatever filenames you want so long as they are given a `.md` extension.

Html files are generated for your content.  The processing is guided by your `config.ini` and metadata blocks in your markdown sources.

[Markdown Basics]: https://help.github.com/articles/markdown-basics/
[Pandoc User Guide]: http://pandoc.org/README.html


*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *


Metadata
--------

Metadata can be placed at the top of a markdown file.  The metadata block should be bounded by a `---` at the top and a `...` at the bottom.

Metadata fields recognized by bassclef include

  * title, subtitle
  * description - a description of the content, 155 characters max
  * date - in whatever format
  * updated - date, in whatever format
  * publisher - name of the original publisher of the content 
  * source - url for the original publication of the content 
  * image - URL for an image file
  * caption - caption for the image

and

  * showtitle - flags that title block should be shown (default
    True)
  * showsocial - flags that social buttons should be shown (default
    True) 

Here is an example metadata block from one of the [articles] on my Web site:

```
---
title: Echoes of Walkerton in Environment Canada cuts
subtitle: Health and safety of Canadians is at risk with latest slashing of Environment Canada budget.
date: 19 March 2014
publisher: The Toronto Star
source: https://www.thestar.com/opinion/commentary/2014/03/19/echoes_of_walkerton_in_environment_canada_cuts.html
image: /images/thumbs/2014-03-19_thestar.png
caption: As seen in [The Toronto Star][0].
...
```

There are no required fields.

You may define your own metadata fields.  Note, however, that all names in the config.ini are reserved, as are the following:

  * titleclass
  * permalink

[articles]: http://tomduck.ca/commentary/2014-03-19_echoes-of-walkerton.html


*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *


Images
------

The image described in your metadata block will be inserted between the first and second elements of your content.  It is also used to construct tags for Facebook, Google Plus and Twitter.  For better control, mark where the image should be inserted using a `<!-- image -->` tag (on its own line).


High-resolution images should be stored in the `images/` folder.  These images are copied to `www/images` during the build process.  Large thumbnails are generated and stored in `www/images/thumbs/`.  You should link to the thumbs from your content.

SVG images are handled separately because of the vector format.  They should be placed in `images/svg/`.  The build process writes png versions into the `www/images/thumbs/` and `www/images/icons/` directories.


*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *


Composed pages
--------------

Bassclef supports the generation of composed pages via `.md.in` files.  These are used to create temporary `.md` files from which `.html` files are generated.  Composed pages can be used to generate a blog.

The composed page should consist of ordinary markdown and filename lines.  If the filenames refer to `.md` content files, then they are read, processed and inserted; otherwise they are printed out as-is.

Normally the entire content of the referenced file is inserted.  You can use `<!-- break -->` in the file being inserted to indicate that any remaining content be truncated.  "Read more..." links are automatically added to the composed page.


*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *


<nav>
[<< Getting Started](/docs/getting-started.html) |
[Top](/docs/index.html) |
[Building and Testing >>](/docs/building-and-testing.html)
</nav>
