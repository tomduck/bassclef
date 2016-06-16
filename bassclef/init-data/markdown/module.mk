
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
DEST_HTML = $(patsubst markdown/%.md,$(OUT)/%.html,$(SOURCE_MD)) \
              $(patsubst $(TMP)/%.md,$(OUT)/%.html,$(DEST_MD))
DEST_XML = $(patsubst markdown/%.md.in,$(OUT)/%.xml,$(SOURCE_MD_IN))


# Functions -------------------------------------------------------------------

# $(call makevars,mdpath,htmlpath): makes variables needed to assemble flags
define makevars
TEMPLATE = $(shell pandoc-tpp -t $(shell $(call getmeta,$(1),template)))
HTMLPATH = $(patsubst $(WWW)/%,/%,$(2))
URL = $$(shell $(PYTHON3) -c "from bassclef.util import absurl;\
                              print(absurl('$$(HTMLPATH)'))")
QUOTEDURL = $$(shell $(PYTHON3) -c \
    "from urllib.parse import quote; \
     print(quote('$$(URL)').replace('/', '%2F'))")
endef

# $(call addflags,mdpath,htmlpath): Adds flags to PANDOCFLAGS
define addflags
$(call makevars,$(1),$(2))
ifneq ($$(TEMPLATE),)
  PANDOCFLAGS += --template $$(TEMPLATE)
endif
PANDOCFLAGS += -M url=$$(URL)
PANDOCFLAGS += -M quoted-url=$$(QUOTEDURL)
endef

# $(call md2html,src.md,dest.html): transforms markdown to html using pandoc
define md2html
@if [ ! -d $(dir $(2)) ]; then mkdir -p $(dir $(2)); fi;
$(eval $(call addflags,$<,$@))
bcms preprocess $(1) | $(PANDOC) $(PANDOCFLAGS) | bcms postprocess > $(2);
endef


# Build rules -----------------------------------------------------------------

PANDOCFLAGS = -s -S \
              -f markdown-markdown_in_html_blocks \
              -t html5 \
              --email-obfuscation=none

markdown: $(DEST_MD)

$(TMP)/%.md: markdown/%.md.in $(SOURCE_MD)
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	bcms compose $< > $@


html: $(DEST_HTML)

$(OUT)/%.html: $(TMP)/%.md
	$(call md2html,$<,$@)

$(OUT)/%.html: markdown/%.md
	$(call md2html,$<,$@)


rss: $(DEST_XML)

$(OUT)/%.xml: markdown/%.md.in $(DEST_HTML)
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	bcms feed $< > $@


# Targets ---------------------------------------------------------------------

ALL += markdown html
CLEAN += $(DEST_MD) $(DEST_HTML) $(DEST_XML)
