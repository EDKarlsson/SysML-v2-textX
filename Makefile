# Usage
# make				# Build parser
# make clean		# remove all generated files
# make simple_test			# Run tests and validate grammars

.PHONY = all clean print

#
PYTHON_BIN := $(shell which python)
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
KERML := $(ROOT_DIR)/kerml

# KerML
CORE:=$(KERML)/core
KERNEL:=$(KERML)/kernel
ROOT:=$(KERML)/root


kerml-root:
	$(PYTHON_BIN) $(KERML)/kerml.py root

print:
	@echo ${ROOT_DIR}
	ls -la $?
