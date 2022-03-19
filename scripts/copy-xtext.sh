#!/usr/bin/env bash

pilot_impl_dir="/Users/dank/git/systems-modeling/SysML-v2-Pilot-Implementation"

sysml_xtext="/org.omg.sysml.xtext/src/org/omg/sysml/xtext/SysML.xtext"
kerml_xtext="/org.omg.kerml.xtext/src/org/omg/kerml/xtext/KerML.xtext"
kerml_expression_xtext="/org.omg.kerml.expressions.xtext/src/org/omg/kerml/expressions/xtext/KerMLExpressions.xtext"
owl_xtext="/org.omg.kerml.owl/src/org/omg/kerml/owl/Owl.xtext"

grammar_xtext="./grammar/xtext"

cp ${pilot_impl_dir}/${sysml_xtext} "${grammar_xtext}"
cp ${pilot_impl_dir}/${kerml_xtext} "${grammar_xtext}"
cp ${pilot_impl_dir}/${kerml_expression_xtext} "${grammar_xtext}"
cp ${pilot_impl_dir}/${owl_xtext} "${grammar_xtext}"
