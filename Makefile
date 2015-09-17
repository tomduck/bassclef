
# Copyright 2015 Thomas J. Duck

# This file is part of bassclef.
#
#  bassclef is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License verson 3 as
#  published by the Free Software Foundation.
#
#  bassclef is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with bassclef.  If not, see <http://www.gnu.org/licenses/>.


# Preamble -------------------------------------------------------------------

# Exits if errors occur in a pipe chain
SHELL = /bin/bash -o pipefail

# Clean up on error (https://www.gnu.org/software/make/manual/make.html#Errors)
.DELETE_ON_ERROR:


# Source files ---------------------------------------------------------------

SOURCE_MD_IN = $(wildcard content/*.md.in) $(wildcard content/*/*.md.in)
SOURCE_MD = $(wildcard content/*.md)  $(wildcard content/*/*.md)

SOURCE_OPENSANS_FONTS =  $(wildcard submodules/open-sans/fonts/*/*)
SOURCE_FONTAWESOME_FONTS =  $(wildcard submodules/font-awesome/fonts/*)

SOURCE_SKELETON_CSS = $(wildcard submodules/skeleton/css/*.css)
SOURCE_FONTAWESOME_CSS = $(wildcard submodules/font-awesome/css/*)

SOURCE_IMG = $(wildcard images/*.*)
SOURCE_SVG = $(wildcard images/svg/*.*)


# Target files ---------------------------------------------------------------

TARGET_MD = $(patsubst content/%.md.in,tmp/%.md,$(SOURCE_MD_IN))

TARGET_HTML = $(patsubst content/%.md,www/%.html,$(SOURCE_MD)) \
              $(patsubst tmp/%.md,www/%.html,$(TARGET_MD))

TARGET_OPENSANS_FONTS = $(patsubst submodules/open-sans/fonts/%,\
                       www/fonts/open-sans/%,$(SOURCE_OPENSANS_FONTS))
TARGET_FONTAWESOME_FONTS = $(patsubst submodules/font-awesome/fonts/%,\
                           www/fonts/Font-Awesome/%,\
                           $(SOURCE_FONTAWESOME_FONTS))

TARGET_CUSTOM_CSS = www/css/custom.css
TARGET_SKELETON_CSS = $(patsubst submodules/skeleton/%,www/%,\
                      $(SOURCE_SKELETON_CSS))
TARGET_OPENSANS_CSS = www/css/open-sans.css
TARGET_FONTAWESOME_CSS = $(patsubst submodules/font-awesome/%,www/%,\
                         $(SOURCE_FONTAWESOME_CSS))

TARGET_IMG = $(patsubst %,www/%,$(SOURCE_IMG)) \
             $(patsubst %,www/%,$(SOURCE_SVG))
TARGET_THUMBS = $(patsubst images/%,www/images/thumbs/%,$(SOURCE_IMG)) \
                $(patsubst images/svg/%.svg,www/images/thumbs/%.png,\
                  $(SOURCE_SVG))
TARGET_ICONS = $(patsubst images/svg/%.svg,www/images/icons/%.png,\
                 $(SOURCE_SVG))


# Functions ------------------------------------------------------------------

define copyfiles
@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi;
@if [ -f $< ]; then echo "cp $< $@"; fi;
@if [ -f $< ]; then cp $< $@; fi;
endef

define md2html
@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi;
scripts/preprocess.py $< | \
    pandoc -s -S \
           -f markdown\
           -t html5 \
           --email-obfuscation=none \
           --template templates/default.html5 \
           --css /css/normalize.css \
           --css /css/skeleton.css \
           --css /css/open-sans.css \
           --css /css/font-awesome.min.css \
           --css /css/custom.css | \
    scripts/postprocess.py > $@;
endef


# Build rules ----------------------------------------------------------------

all: markdown html css fonts images


markdown: $(TARGET_MD)

tmp/%.md: content/%.md.in $(SOURCE_MD) \
          scripts/makesection.py scripts/preprocess.py
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	scripts/makesection.py $< > $@


html: $(TARGET_HTML)

www/%.html: tmp/%.md scripts/preprocess.py scripts/postprocess.py \
            templates/default.html5 config.ini
	$(md2html)

www/%.html: content/%.md scripts/preprocess.py scripts/postprocess.py \
            templates/default.html5 config.ini
	$(md2html)


css: $(TARGET_CUSTOM_CSS) $(TARGET_SKELETON_CSS) $(TARGET_OPENSANS_CSS) \
     $(TARGET_FONTAWESOME_CSS)

www/css/custom.css: css/custom.css
	$(copyfiles)

www/css/%.css: submodules/skeleton/css/%.css
	$(copyfiles)

www/css/open-sans.css: submodules/open-sans/open-sans.css
	$(copyfiles)

www/css/font-awesome%: submodules/font-awesome/css/font-awesome%
	$(copyfiles)


fonts: $(TARGET_OPENSANS_FONTS) $(TARGET_FONTAWESOME_FONTS)

www/fonts/open-sans/%: submodules/open-sans/fonts/%
	$(copyfiles)

www/fonts/Font-Awesome/%: submodules/font-awesome/fonts/%
	$(copyfiles)


images: $(TARGET_IMG) $(TARGET_THUMBS) $(TARGET_ICONS)

www/images/icons/%.png: images/svg/%.svg
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	convert $< -resize x50 $@

www/images/thumbs/%.png: images/svg/%.svg
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	convert $< -resize 250x $@

www/images/thumbs/%: images/%
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	convert $< -resize 250x $@

www/%: %
	$(copyfiles)


# Deploy rules ---------------------------------------------------------------

serve:
	cd www && python -m SimpleHTTPServer


# Housekeeping rules ---------------------------------------------------------

# Don't delete the www directory!  The installed site has additional
# directories (e.g., piwik) that must remain.

clean:
	rm -f www/*.html
	rm -rf www/posts
	rm -rf www/commentary
	rm -rf www/css
	rm -rf www/fonts
	rm -rf www/images
	rm -rf tmp

.PHONY: markdown html css fonts images serve clean
