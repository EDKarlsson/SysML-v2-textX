#!/usr/bin/env bash

#find . -name '*.dot' -print -exec rm {} \;

root_tx=$(find . -name 'root.tx')
textx generate "${root_tx}" --target dot

root_dots=$(find . -name '*.dot')
#open root.dot.png