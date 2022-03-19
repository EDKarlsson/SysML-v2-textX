#!/usr/bin/env bash

release_dir="/Users/dank/git/systems-modeling/SysML-v2-Release"
sysml_libs=${release_dir}/"sysml.library"
kernel_lib="Kernel Library"
domain_lib="Domain Libraries"
systems_lib="Systems Library"

proj_lib_kernel="./libs/kernel"
proj_lib_sysml="./libs/sysml"
proj_lib_domain="./libs/domain"

mkdir "${proj_lib_domain}"
mkdir "${proj_lib_sysml}"
mkdir "${proj_lib_kernel}"

cp ${sysml_libs}/"${kernel_lib}"/* ${proj_lib_kernel}
cp ${sysml_libs}/"${domain_lib}"/* ${proj_lib_domain}
cp ${sysml_libs}/"${systems_lib}"/* ${proj_lib_sysml}

