
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

SOURCE_OPENSANS_FONTS =  $(wildcard fonts/open-sans/*/*.*)
SOURCE_FONTAWESOME_FONTS =  $(wildcard fonts/font-awesome/*.*)


# Destination files -----------------------------------------------------------

DEST_OPENSANS_FONTS = $(patsubst fonts/open-sans/%,\
                        www$(WEBROOT)/fonts/open-sans/%,\
                        $(SOURCE_OPENSANS_FONTS))

DEST_FONTAWESOME_FONTS = $(patsubst fonts/font-awesome/%,\
                           www$(WEBROOT)/fonts/font-awesome/%,\
                           $(SOURCE_FONTAWESOME_FONTS))


# Build rules -----------------------------------------------------------------

fonts: $(DEST_OPENSANS_FONTS) $(DEST_FONTAWESOME_FONTS)

www$(WEBROOT)/fonts/open-sans/%: fonts/open-sans/%
	$(call copyfiles,$<,$@)

www$(WEBROOT)/fonts/font-awesome/%: fonts/font-awesome/%
	$(call copyfiles,$<,$@)


# Targets ---------------------------------------------------------------------

ALL += fonts
CLEAN += $(DEST_OPENSANS_FONTS) $(DEST_FONTAWESOME_FONTS)
