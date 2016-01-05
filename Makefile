
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

# Paths
WEBROOT = $(shell python3 -c "from scripts import util; print(util.config('webroot'));")
TMP := $(shell mktemp -d /tmp/bassclef.XXXXXXXXXX)

# Error checking
ifeq ($(TMP),)
$(error Temporary directory could not be created.)
endif


# Source files ---------------------------------------------------------------

SOURCE_MD_IN = $(wildcard markdown/*.md.in) $(wildcard markdown/*/*.md.in)
SOURCE_MD = $(wildcard markdown/*.md) $(wildcard markdown/*/*.md)

SOURCE_OPENSANS_FONTS =  $(wildcard submodules/open-sans/fonts/*/*)
SOURCE_FONTAWESOME_FONTS =  $(wildcard submodules/font-awesome/fonts/*)

SOURCE_BASSCLEF_CSS = $(wildcard css/*.css)
SOURCE_SKELETON_CSS = $(wildcard submodules/skeleton/css/*.css)
SOURCE_FONTAWESOME_CSS = $(wildcard submodules/font-awesome/css/*)

SOURCE_IMG = $(wildcard images/*.*)


# Target files ---------------------------------------------------------------

TARGET_MD = $(patsubst markdown/%.md.in,$(TMP)/%.md,$(SOURCE_MD_IN))

TARGET_HTML = $(patsubst markdown/%.md,www$(WEBROOT)/%.html,$(SOURCE_MD)) \
              $(patsubst $(TMP)/%.md,www$(WEBROOT)/%.html,$(TARGET_MD))

TARGET_XML = $(patsubst markdown/%.md.in,www$(WEBROOT)/%.xml,$(SOURCE_MD_IN))


TARGET_OPENSANS_FONTS = $(patsubst submodules/open-sans/fonts/%,\
                          www$(WEBROOT)/fonts/open-sans/%,\
                          $(SOURCE_OPENSANS_FONTS))

TARGET_FONTAWESOME_FONTS = $(patsubst submodules/font-awesome/fonts/%,\
                             www$(WEBROOT)/fonts/font-awesome/%,\
                             $(SOURCE_FONTAWESOME_FONTS))


TARGET_BASSCLEF_CSS = $(patsubst css/%,\
                      www$(WEBROOT)/css/%,\
                      $(SOURCE_BASSCLEF_CSS))

TARGET_SKELETON_CSS = $(patsubst submodules/skeleton/%,\
                        www$(WEBROOT)/%,\
                        $(SOURCE_SKELETON_CSS))

TARGET_OPENSANS_CSS = www$(WEBROOT)/css/open-sans.css

TARGET_FONTAWESOME_CSS = $(patsubst submodules/font-awesome/%,\
                           www$(WEBROOT)/%,\
                           $(SOURCE_FONTAWESOME_CSS))


TARGET_IMG = $(patsubst %,www$(WEBROOT)/%,$(SOURCE_IMG))

TARGET_SIZED = $(patsubst images/%,www$(WEBROOT)/images/sized/%,$(SOURCE_IMG))


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
           --css $(WEBROOT)/css/normalize.css \
           --css $(WEBROOT)/css/skeleton.css \
           --css $(WEBROOT)/css/open-sans.css \
           --css $(WEBROOT)/css/font-awesome.min.css \
           --css $(WEBROOT)/css/bassclef.css | \
    scripts/postprocess.py > $@;
endef


# Build rules ----------------------------------------------------------------

all: markdown html rss css fonts images


markdown: $(TARGET_MD)

$(TMP)/%.md: markdown/%.md.in $(SOURCE_MD) \
          scripts/compose.py scripts/preprocess.py
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	scripts/compose.py $< > $@


html: $(TARGET_HTML)

www$(WEBROOT)/%.html: $(TMP)/%.md scripts/preprocess.py \
                         scripts/postprocess.py \
                         scripts/util.py templates/default.html5 config.ini
	$(md2html)

www$(WEBROOT)/%.html: markdown/%.md scripts/preprocess.py \
                         scripts/postprocess.py \
                         scripts/util.py templates/default.html5 config.ini
	$(md2html)


rss: $(TARGET_XML)

www$(WEBROOT)/%.xml: markdown/%.md.in $(TARGET_HTML) scripts/feed.py
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	scripts/feed.py $< > $@


css: $(TARGET_BASSCLEF_CSS) $(TARGET_SKELETON_CSS) $(TARGET_OPENSANS_CSS) \
     $(TARGET_FONTAWESOME_CSS)

www$(WEBROOT)/css/%: css/%
	$(copyfiles)

www$(WEBROOT)/css/%.css: submodules/skeleton/css/%.css
	$(copyfiles)

www$(WEBROOT)/css/open-sans.css: submodules/open-sans/open-sans.css
	$(copyfiles)

www$(WEBROOT)/css/font-awesome%: submodules/font-awesome/css/font-awesome%
	$(copyfiles)


fonts: $(TARGET_OPENSANS_FONTS) $(TARGET_FONTAWESOME_FONTS)

www$(WEBROOT)/fonts/open-sans/%: submodules/open-sans/fonts/%
	$(copyfiles)

www$(WEBROOT)/fonts/font-awesome/%: submodules/font-awesome/fonts/%
	$(copyfiles)


images: $(TARGET_IMG) $(TARGET_SIZED)

www$(WEBROOT)/images/sized/%: images/%
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	convert $< -resize 250x $@

www$(WEBROOT)/%: %
	$(copyfiles)


# Deploy rules ---------------------------------------------------------------

serve:
	cd www && python -m SimpleHTTPServer


# Housekeeping rules ---------------------------------------------------------

# Don't delete the www directory!  The installed site has additional
# directories (e.g., piwik) that must remain.

clean:
	rm -f www$(WEBROOT)/*.html
	rm -f www$(WEBROOT)/*.xml
	rm -rf www$(WEBROOT)/css
	rm -rf www$(WEBROOT)/fonts
	rm -rf www$(WEBROOT)/images

.PHONY: markdown html css fonts images serve clean
