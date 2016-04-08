
# Source files ----------------------------------------------------------------

SOURCE_MD_IN = $(wildcard markdown/*.md.in) $(wildcard markdown/*/*.md.in)
SOURCE_MD = $(wildcard markdown/*.md) $(wildcard markdown/*/*.md)


# Destination files -----------------------------------------------------------

DEST_MD = $(patsubst markdown/%.md.in,$(TMP)/%.md,$(SOURCE_MD_IN))
DEST_HTML = $(patsubst markdown/%.md,www$(WEBROOT)/%.html,$(SOURCE_MD)) \
              $(patsubst $(TMP)/%.md,www$(WEBROOT)/%.html,$(DEST_MD))
DEST_XML = $(patsubst markdown/%.md.in,www$(WEBROOT)/%.xml,$(SOURCE_MD_IN))


# Functions -------------------------------------------------------------------

define md2html
@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi;
$(PYTHON3) scripts/preprocess.py $< | \
    $(PANDOC) -s -S \
           -f markdown-markdown_in_html_blocks\
           -t html5 \
           --email-obfuscation=none \
           --template templates/default.html5 \
           --css /css/normalize.css \
           --css /css/skeleton.css \
           --css /css/open-sans.css \
           --css /css/font-awesome.min.css \
           --css /css/bassclef.css | \
    $(PYTHON3) scripts/postprocess.py > $@;
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
	$(md2html)

www$(WEBROOT)/%.html: markdown/%.md scripts/preprocess.py \
                         scripts/postprocess.py \
                         scripts/util.py templates/default.html5 config.ini
	$(md2html)


rss: $(DEST_XML)

www$(WEBROOT)/%.xml: markdown/%.md.in $(DEST_HTML) scripts/feed.py
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	$(PYTHON3) scripts/feed.py $< > $@


# Targets ---------------------------------------------------------------------

ALL += markdown html rss
CLEAN += $(DEST_MD) $(DEST_HTML) $(DEST_XML)
