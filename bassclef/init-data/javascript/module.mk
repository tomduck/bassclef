
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

SOURCE_JS = $(wildcard javascript/*.js) $(wildcard javascript/*/*.js)


# Destination files -----------------------------------------------------------

DEST_JS = $(patsubst javascript/%,www$(WEBROOT)/javascript/%,$(SOURCE_JS))


# Build rules -----------------------------------------------------------------

javascript: $(DEST_JS)

www$(WEBROOT)/javascript/%: javascript/%
	$(call copyfiles,$<,$@)


# Targets ---------------------------------------------------------------------

ALL += javascript
CLEAN += $(DEST_JS)
