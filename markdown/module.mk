
# Copyright 2015, 2016 Thomas J. Duck <tomduck@tomduck.ca>

# This file is part of bassclef.
#
#  Bassclef is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License verson 3 as
#  published by the Free Software Foundation.
#
#  Bassclef is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with bassclef.  If not, see <http://www.gnu.org/licenses/>.


# Source files ----------------------------------------------------------------

SOURCE_MD_IN = $(wildcard markdown/*.md.in) $(wildcard markdown/*/*.md.in)
SOURCE_MD = $(wildcard markdown/*.md) $(wildcard markdown/*/*.md)


# Destination files -----------------------------------------------------------

DEST_MD = $(patsubst markdown/%.md.in,$(TMP)/%.md,$(SOURCE_MD_IN))
DEST_HTML = $(patsubst markdown/%.md,www$(WEBROOT)/%.html,$(SOURCE_MD)) \
              $(patsubst $(TMP)/%.md,www$(WEBROOT)/%.html,$(DEST_MD))
DEST_XML = $(patsubst markdown/%.md.in,www$(WEBROOT)/%.xml,$(SOURCE_MD_IN))


# Functions -------------------------------------------------------------------

# $(call md2html,src.md,dest.html): transforms markdown to html using pandoc
define md2html
@if [ ! -d $(dir $(2)) ]; then mkdir -p $(dir $(2)); fi;
$(PYTHON3) scripts/preprocess.py $(1) | \
    $(PANDOC) -s -S \
           -f markdown-markdown_in_html_blocks\
           -t html5 \
           --email-obfuscation=none \
           --template $(shell $(call getmeta,template)) \
           --css /css/normalize.css \
           --css /css/skeleton.css \
           --css /css/open-sans.css \
           --css /css/font-awesome.min.css \
           --css /css/bassclef.css | \
    $(PYTHON3) scripts/postprocess.py > $(2);
endef


# Build rules -----------------------------------------------------------------

markdown: $(DEST_MD)

$(TMP)/%.md: markdown/%.md.in $(SOURCE_MD) \
          scripts/compose.py scripts/preprocess.py
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	$(PYTHON3) scripts/compose.py $< > $@


html: $(DEST_HTML)

www$(WEBROOT)/%.html: $(TMP)/%.md scripts/preprocess.py \
                         scripts/postprocess.py \
                         scripts/util.py templates/default.html5 config.ini
	$(call md2html,$<,$@)

www$(WEBROOT)/%.html: markdown/%.md scripts/preprocess.py \
                         scripts/postprocess.py \
                         scripts/util.py templates/default.html5 config.ini
	$(call md2html,$<,$@)


rss: $(DEST_XML)

www$(WEBROOT)/%.xml: markdown/%.md.in $(DEST_HTML) scripts/feed.py
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	$(PYTHON3) scripts/feed.py $< > $@


# Targets ---------------------------------------------------------------------

ALL += markdown html rss
CLEAN += $(DEST_MD) $(DEST_HTML) $(DEST_XML)
