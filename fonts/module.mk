
# Source files ----------------------------------------------------------------

SOURCE_OPENSANS_FONTS =  $(wildcard submodules/open-sans/fonts/*/*)
SOURCE_FONTAWESOME_FONTS =  $(wildcard submodules/font-awesome/fonts/*)


# Destination files -----------------------------------------------------------

DEST_OPENSANS_FONTS = $(patsubst submodules/open-sans/fonts/%,\
                        www$(WEBROOT)/fonts/open-sans/%,\
                        $(SOURCE_OPENSANS_FONTS))

DEST_FONTAWESOME_FONTS = $(patsubst submodules/font-awesome/fonts/%,\
                           www$(WEBROOT)/fonts/font-awesome/%,\
                           $(SOURCE_FONTAWESOME_FONTS))


# Build rules -----------------------------------------------------------------

fonts: $(DEST_OPENSANS_FONTS) $(DEST_FONTAWESOME_FONTS)

www$(WEBROOT)/fonts/open-sans/%: submodules/open-sans/fonts/%
	$(copyfiles)

www$(WEBROOT)/fonts/font-awesome/%: submodules/font-awesome/fonts/%
	$(copyfiles)


# Targets ---------------------------------------------------------------------

ALL += fonts
CLEAN += $(DEST_OPENSANS_FONTS) $(DEST_FONTAWESOME_FONTS)
