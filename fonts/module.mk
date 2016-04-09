
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
