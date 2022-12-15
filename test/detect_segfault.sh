#!/bin/bash

# I read the post here: https://unix.stackexchange.com/a/24344,
# for a script to capture seg fault when running my program.

# This script sets a "trap" for status 139 (the status of seg
# fault), so if/when the program that is passed as argument to
# this script ($1) generates it, the script will output "139".
# This script is to be called as a subroutine in my python
# program, to detect a buggy version of my program.

set -e
trap 'case $? in
        139) echo $?;;
      esac' EXIT
./$1