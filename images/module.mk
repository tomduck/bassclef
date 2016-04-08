
# Source files ----------------------------------------------------------------

SOURCE_IMG = $(filter-out images/module.mk,$(wildcard images/*.*))


# Destination files -----------------------------------------------------------

DEST_IMG = $(patsubst %,www$(WEBROOT)/%,$(SOURCE_IMG))
DEST_TILE = $(patsubst images/%,www$(WEBROOT)/images/tiles/%,$(SOURCE_IMG))


# Build rules -----------------------------------------------------------------

images: $(DEST_IMG) $(DEST_TILE)

www$(WEBROOT)/images/tiles/%: images/%
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	$(CONVERT) $< -resize 250x $@

www$(WEBROOT)/%: %
	$(copyfiles)


# Targets ---------------------------------------------------------------------

ALL += images
CLEAN += $(DEST_IMG) $(DEST_TILE)
