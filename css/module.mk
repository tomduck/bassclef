
# Source files ----------------------------------------------------------------

SOURCE_BASSCLEF_CSS = $(wildcard css/*.css)
SOURCE_SKELETON_CSS = $(wildcard submodules/skeleton/css/*.css)
SOURCE_FONTAWESOME_CSS = $(wildcard submodules/font-awesome/css/*)


# Destination files -----------------------------------------------------------

DEST_BASSCLEF_CSS = $(patsubst css/%,\
                      www$(WEBROOT)/css/%,\
                      $(SOURCE_BASSCLEF_CSS))

DEST_SKELETON_CSS = $(patsubst submodules/skeleton/%,\
                      www$(WEBROOT)/%,\
                      $(SOURCE_SKELETON_CSS))

DEST_OPENSANS_CSS = www$(WEBROOT)/css/open-sans.css

DEST_FONTAWESOME_CSS = $(patsubst submodules/font-awesome/%,\
                           www$(WEBROOT)/%,\
                           $(SOURCE_FONTAWESOME_CSS))


# Build rules -----------------------------------------------------------------

css: $(DEST_BASSCLEF_CSS) $(DEST_SKELETON_CSS) $(DEST_OPENSANS_CSS) \
     $(DEST_FONTAWESOME_CSS)

www$(WEBROOT)/css/%: css/%
	$(copyfiles)

www$(WEBROOT)/css/%.css: submodules/skeleton/css/%.css
	$(copyfiles)

www$(WEBROOT)/css/open-sans.css: submodules/open-sans/open-sans.css
	$(copyfiles)

www$(WEBROOT)/css/font-awesome%: submodules/font-awesome/css/font-awesome%
	$(copyfiles)


# Targets ---------------------------------------------------------------------

ALL += css
CLEAN += $(DEST_BASSCLEF_CSS) $(DEST_SKELETON_CSS) $(DEST_OPENSANS_CSS) \
         $(DEST_FONTAWESOME_CSS)
