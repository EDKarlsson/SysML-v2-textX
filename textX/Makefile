# Usage
# make				# Build parser
# make clean		# remove all generated files
# make test			# Run tests and validate grammars

.PHONY = all clean print

#
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
SRC := $(ROOT_DIR)/src
KERML := $(ROOT_DIR)/kerml
COMMON := $(ROOT_DIR)/common

# KerML
CORE:=$(KERML)/core
KERNEL:=$(KERML)/kernel
ROOT:=$(KERML)/root

GRAMMAR_DIR = $(ROOT_DIR)/grammar
LIBS = $(ROOT_DIR)/libs

COMMON_TX = $(wildcard ./common/*.tx)


print:
	@echo ${ROOT_DIR}
	ls -la $?
