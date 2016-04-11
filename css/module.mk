
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

www$(WEBROOT)/css/%: css/% \
                     css/module.mk
	$(call copyfiles,$<,$@)

www$(WEBROOT)/css/%.css: submodules/skeleton/css/%.css \
                         css/module.mk
	$(call copyfiles,$<,$@)

www$(WEBROOT)/css/open-sans.css: submodules/open-sans/open-sans.css \
                                 css/module.mk
	$(call copyfiles,$<,$@)

www$(WEBROOT)/css/font-awesome%: submodules/font-awesome/css/font-awesome% \
                                 css/module.mk
	$(call copyfiles,$<,$@)


# Targets ---------------------------------------------------------------------

ALL += css
CLEAN += $(DEST_BASSCLEF_CSS) $(DEST_SKELETON_CSS) $(DEST_OPENSANS_CSS) \
         $(DEST_FONTAWESOME_CSS)
