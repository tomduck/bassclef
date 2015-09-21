
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

# Directories
SRC = $(shell python3 -c "from scripts import util; print(util.config('srcdir'));")
WWW = $(shell python3 -c "from scripts import util; print(util.config('wwwdir'));")
TMP := $(shell mktemp -d /tmp/bassclef.XXXXXXXXXX)

# Error checking
ifeq ($(TMP),)
$(error Temporary directory could not be created.)
endif


# Source files ---------------------------------------------------------------

SOURCE_MD_IN = $(wildcard content/*.md.in) $(wildcard content/*/*.md.in)
SOURCE_MD = $(wildcard content/*.md) $(wildcard content/*/*.md) \
            $(wildcard doc/*.md)

SOURCE_OPENSANS_FONTS =  $(wildcard submodules/open-sans/fonts/*/*)
SOURCE_FONTAWESOME_FONTS =  $(wildcard submodules/font-awesome/fonts/*)

SOURCE_BASSCLEF_CSS = $(wildcard css/*.css)
SOURCE_SKELETON_CSS = $(wildcard submodules/skeleton/css/*.css)
SOURCE_FONTAWESOME_CSS = $(wildcard submodules/font-awesome/css/*)

SOURCE_IMG = $(wildcard images/*.*)
SOURCE_SVG = $(wildcard images/svg/*.*)


# Target files ---------------------------------------------------------------

TARGET_MD = $(patsubst content/%.md.in,$(TMP)/%.md,$(SOURCE_MD_IN))

TARGET_HTML = $(patsubst content/%.md,$(WWW)/%.html,$(SOURCE_MD)) \
              $(patsubst $(TMP)/%.md,$(WWW)/%.html,$(TARGET_MD))
TARGET_DOC = $(patsubst doc/%.md,$(WWW)/doc/%.html,$(SOURCE_MD))

TARGET_OPENSANS_FONTS = $(patsubst submodules/open-sans/fonts/%,\
                       $(WWW)/fonts/open-sans/%,$(SOURCE_OPENSANS_FONTS))
TARGET_FONTAWESOME_FONTS = $(patsubst submodules/font-awesome/fonts/%,\
                           $(WWW)/fonts/font-awesome/%,\
                           $(SOURCE_FONTAWESOME_FONTS))

TARGET_BASSCLEF_CSS = $(patsubst css/%,$(WWW)/css/%,$(SOURCE_BASSCLEF_CSS))
TARGET_SKELETON_CSS = $(patsubst submodules/skeleton/%,$(WWW)/%,\
                      $(SOURCE_SKELETON_CSS))
TARGET_OPENSANS_CSS = $(WWW)/css/open-sans.css
TARGET_FONTAWESOME_CSS = $(patsubst submodules/font-awesome/%,$(WWW)/%,\
                         $(SOURCE_FONTAWESOME_CSS))

TARGET_IMG = $(patsubst %,$(WWW)/%,$(SOURCE_IMG)) \
             $(patsubst %,$(WWW)/%,$(SOURCE_SVG))
TARGET_SIZED = $(patsubst images/%,$(WWW)/images/sized/%,$(SOURCE_IMG)) \
               $(patsubst images/svg/%.svg,$(WWW)/images/sized/%.png,\
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
           --css /css/bassclef.css | \
    scripts/postprocess.py > $@;
endef


# Build rules ----------------------------------------------------------------

all: markdown html css fonts images


markdown: $(TARGET_MD)

$(TMP)/%.md: content/%.md.in $(SOURCE_MD) \
          scripts/compose.py scripts/preprocess.py
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	scripts/compose.py $< > $@


html: $(TARGET_HTML)

$(WWW)/%.html: $(TMP)/%.md scripts/preprocess.py scripts/postprocess.py \
            scripts/util.py templates/default.html5 config.ini
	$(md2html)

$(WWW)/%.html: content/%.md scripts/preprocess.py scripts/postprocess.py \
            scripts/util.py templates/default.html5 config.ini
	$(md2html)


doc: $(TARGET_DOC)

$(WWW)/doc/%.html: doc/%.md scripts/preprocess.py scripts/postprocess.py \
            scripts/util.py templates/default.html5 config.ini
	$(md2html)



css: $(TARGET_BASSCLEF_CSS) $(TARGET_SKELETON_CSS) $(TARGET_OPENSANS_CSS) \
     $(TARGET_FONTAWESOME_CSS)

$(WWW)/css/%: css/%
	$(copyfiles)

$(WWW)/css/%.css: submodules/skeleton/css/%.css
	$(copyfiles)

$(WWW)/css/open-sans.css: submodules/open-sans/open-sans.css
	$(copyfiles)

$(WWW)/css/font-awesome%: submodules/font-awesome/css/font-awesome%
	$(copyfiles)


fonts: $(TARGET_OPENSANS_FONTS) $(TARGET_FONTAWESOME_FONTS)

$(WWW)/fonts/open-sans/%: submodules/open-sans/fonts/%
	$(copyfiles)

$(WWW)/fonts/font-awesome/%: submodules/font-awesome/fonts/%
	$(copyfiles)


images: $(TARGET_IMG) $(TARGET_SIZED)

$(WWW)/images/sized/%.png: images/svg/%.svg
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	convert $< -resize 250x $@

$(WWW)/images/sized/%: images/%
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	convert $< -resize 250x $@

$(WWW)/%: %
	$(copyfiles)


# Deploy rules ---------------------------------------------------------------

serve:
	cd $(WWW) && python -m SimpleHTTPServer


# Housekeeping rules ---------------------------------------------------------

# Don't delete the $(WWW) directory!  The installed site has additional
# directories (e.g., piwik) that must remain.

clean:
	rm -f $(WWW)/*.html
	rm -rf $(WWW)/posts
	rm -rf $(WWW)/commentary
	rm -rf $(WWW)/css
	rm -rf $(WWW)/fonts
	rm -rf $(WWW)/images
	rm -rf $(WWW)/doc

.PHONY: markdown html css fonts images serve clean
