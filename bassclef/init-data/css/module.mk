
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

SOURCE_BASSCLEF_CSS = $(wildcard css/*.css)
SOURCE_SKELETON_CSS = $(wildcard css/skeleton/*.css)
SOURCE_OPENSANS_CSS = $(wildcard css/open-sans/*.css)
SOURCE_FONTAWESOME_CSS = $(wildcard css/font-awesome/*.css)


# Destination files -----------------------------------------------------------

DEST_BASSCLEF_CSS = $(patsubst css/%,\
                      www$(WEBROOT)/css/%,\
                      $(SOURCE_BASSCLEF_CSS))

DEST_SKELETON_CSS = $(patsubst css/skeleton/%,\
                      www$(WEBROOT)/css/skeleton/%,\
                      $(SOURCE_SKELETON_CSS))

DEST_OPENSANS_CSS = $(patsubst css/open-sans/%,\
                      www$(WEBROOT)/css/open-sans/%,\
                      $(SOURCE_OPENSANS_CSS))

DEST_FONTAWESOME_CSS = $(patsubst css/font-awesome/%,\
                         www$(WEBROOT)/css/font-awesome/%,\
                         $(SOURCE_FONTAWESOME_CSS))


# Build rules -----------------------------------------------------------------

css: $(DEST_BASSCLEF_CSS) $(DEST_SKELETON_CSS) $(DEST_OPENSANS_CSS) \
     $(DEST_FONTAWESOME_CSS)

www$(WEBROOT)/css/%: css/%
	$(call copyfiles,$<,$@)

www$(WEBROOT)/css/skeleton/%: css/skeleton/%
	$(call copyfiles,$<,$@)

www$(WEBROOT)/css/open-sans/%: css/open-sans/%
	$(call copyfiles,$<,$@)

www$(WEBROOT)/css/font-awesome/%: css/font-awesome/%
	$(call copyfiles,$<,$@)


# Targets ---------------------------------------------------------------------

ALL += css
CLEAN += $(DEST_BASSCLEF_CSS) $(DEST_SKELETON_CSS) $(DEST_OPENSANS_CSS) \
         $(DEST_FONTAWESOME_CSS)
