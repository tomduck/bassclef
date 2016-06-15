
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

SOURCE_CSS = $(wildcard css/*.css) $(wildcard css/*/*.css)


# Destination files -----------------------------------------------------------

DEST_CSS = $(patsubst css/%,www$(WEBROOT)/css/%,$(SOURCE_CSS))


# Build rules -----------------------------------------------------------------

css: $(DEST_CSS)

www$(WEBROOT)/css/%: css/%
	@if [ ! -d $(dir $@) ]; then mkdir -p $(dir $@); fi
	$(call copyfiles,$<,$@)


# Targets ---------------------------------------------------------------------

ALL += css
CLEAN += $(DEST_CSS)
