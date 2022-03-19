#!/usr/bin/env bash

tests=./test

KERML_TESTS=`find ./grammar/`
#syntax-cli --grammar grammar/kerml.sbnf --mode LALR1 --file  "${tests}"/Base.kerml --validate
