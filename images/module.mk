
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
