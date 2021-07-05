##
# Project Makefile for $PROJECT_NAME
#  Project bootstrapping
#  Project automation entry points
#  Project command/control facilities
##
SHELL := bash
MAKEFLAGS += --warn-undefined-variables
.SHELLFLAGS := -euxo pipefail -c
.DEFAULT_GOAL := default

##
# Makefile project context and includes
##

# NOTE: `firstword` below gives top-level Makefile,
# whereas `lastword` gives the last included Makefile.
THIS_MAKEFILE := $(abspath $(firstword $(MAKEFILE_LIST)))

# In case Makefile is a symlink, follow it before we compute
# ${SRC_ROOT}.  We use python because bash `readlink` breaks OSX
THIS_MAKEFILE := `python -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' ${THIS_MAKEFILE}`

# Set root directories, everything else is based on them
SRC_ROOT := $(shell dirname ${THIS_MAKEFILE})
PROJECT_ROOT := ${SRC_ROOT}

##
# lib locations and includes:
# lib submodule should be added with:
#   `git submodule add git@github.com:user/makefiles.git .makefiles`
##
MAKE_INCLUDES_DIR := ${SRC_ROOT}/automation
include ${MAKE_INCLUDES_DIR}/Makefile.base.mk
include ${MAKE_INCLUDES_DIR}/Makefile.yaml.mk
include ${MAKE_INCLUDES_DIR}/Makefile.json.mk
include ${MAKE_INCLUDES_DIR}/Makefile.ssh.mk
include ${MAKE_INCLUDES_DIR}/Makefile.python.mk

# begin local includes
# include ${SRC_ROOT}/Makefile.placeholder.mk

test:
	reactor --help
