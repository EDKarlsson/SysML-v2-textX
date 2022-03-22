# Usage
# make				# Build parser
# make clean		# remove all generated files
# make simple_test			# Run tests and validate grammars

.PHONY = all clean

SYNTAX = syntax-cli
MODE_LALR1 = LALR1
MODE_LR0 = LR0
MODE_LALR1 = SLR1
MODE_LALR1 = LALR1

GRAMMAR_DIR = ./grammar

KERML_GRAMMARS := $(wildcard $(GRAMMAR_DIR)/kerml/*.bnf)
SYSML_GRAMMARS := $(wildcard $(GRAMMAR_DIR)/sysml/*.bnf)

KERML_MODELS := $(wildcard *.kerml)
SYSML_MODELS := $(wildcard *.sysml)

# Rules

all: kerml

#kerml:
#	@echo "Running Syntax on KerML Grammar"
#	${SYNTAX} --grammar grammar/kerml.sbnf --mode LALR1 --file  "${tests}"/basic_kerml.kerml --table

test:
	@echo "Running Tests"
	$(SYNTAX) --grammar $(MODE_LALR1) --file