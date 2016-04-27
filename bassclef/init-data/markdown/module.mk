
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

# $(shell $(call templateflag,path)): constructs the template flag
define templateflag
TEMPLATE=$(shell pandoc-tpp -t $(shell $(call getmeta,$(1),template))); \
if [ -f $$TEMPLATE ]; then echo "--template $$TEMPLATE"; fi;
endef

# $(call md2html,src.md,dest.html): transforms markdown to html using pandoc
define md2html
@if [ ! -d $(dir $(2)) ]; then mkdir -p $(dir $(2)); fi;
bcms preprocess $(1) | \
  $(PANDOC) -s -S \
            -f markdown-markdown_in_html_blocks\
            -t html5 \
            --email-obfuscation=none \
            $(shell $(call templateflag,$(1))) | \
  bcms postprocess > $(2);
endef


# Build rules -----------------------------------------------------------------

markdown: $(DEST_MD)

$(TMP)/%.md: markdown/%.md.in $(SOURCE_MD)
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	bcms compose $< > $@


html: $(DEST_HTML)

www$(WEBROOT)/%.html: $(TMP)/%.md
	$(call md2html,$<,$@)

www$(WEBROOT)/%.html: markdown/%.md
	$(call md2html,$<,$@)


rss: $(DEST_XML)

www$(WEBROOT)/%.xml: markdown/%.md.in $(DEST_HTML)
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	bcms feed $< > $@


# Targets ---------------------------------------------------------------------

ALL += markdown html
CLEAN += $(DEST_MD) $(DEST_HTML) $(DEST_XML)
