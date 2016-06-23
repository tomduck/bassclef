
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


# Preamble -------------------------------------------------------------------

# Exits if errors occur in a pipe chain
SHELL = /bin/bash -o pipefail

# Clean up on error (https://www.gnu.org/software/make/manual/make.html#Errors)
.DELETE_ON_ERROR:

# Executables
PYTHON3 = python3
PANDOC = pandoc
CONVERT = convert

# Variables to store targets from each module
ALL =
CLEAN =


# Functions -------------------------------------------------------------------

# $(shell $(call getconfig,name)): gets value from config.ini
getconfig = $(PYTHON3) -c "from bassclef.util import getconfig;\
                           print(getconfig('$(1)'))"

# $(shell $(call getmeta,file,name)): gets meta value
getmeta = $(PYTHON3) -c "from bassclef.util import getmeta;\
                         print(getmeta('$(1)', '$(2)'))"

# $(call copyfiles,src,dest): copies files from source to destination
define copyfiles
@if [ ! -d $(dir $(2)) ]; then mkdir -p $(dir $(2)); fi;
@if [ -f $(1) ]; then echo "cp $(1) $(2)"; fi;
@if [ -f $(1) ]; then cp $(1) $(2); fi;
endef


# Paths -----------------------------------------------------------------------

WWW = www
WEBROOT = $(shell $(call getconfig,web-root))
ifeq ($(WEBROOT),)
  OUT = $(WWW)
else
  OUT = $(WWW)/$(WEBROOT)
endif

TMP := $(shell mktemp -d /tmp/bassclef.XXXXXXXXXX)
ifeq ($(TMP),)
$(error Temporary directory could not be created.)
endif


# Module imports --------------------------------------------------------------

MODULES = $(wildcard */.module.mk)

include $(MODULES)


# Default rule ---------------------------------------------------------------

.DEFAULT_GOAL =

all: $(ALL)


# Housekeeping rules ---------------------------------------------------------

clean:
	@echo "Removing files and directories from www/..."
	@rm -rf $(CLEAN)
	@if [ -d "www" ]; then find www -type d -empty -delete; fi

.PHONY: $(ALL) serve clean
