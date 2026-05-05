#!/bin/bash
# generate_pywork.sh
# Assembles the pywork/ directory for a given dictionary using generate.py.
#
# Usage: sh generate_pywork.sh <dict> <outdir>
#   <dict>    lowercase dictionary code (e.g. mw, skd)
#   <outdir>  target directory (e.g. ../../MWScan/2020 or tempparent/mw)
#
# Reads inventory.txt to determine which files go into outdir/pywork/:
#   C  — copied verbatim from makotemplates/
#   T  — rendered as a Mako template using dict parameters from dictparms.py
#   CD — copied verbatim from distinctfiles/<dict>/pywork/
#   D  — deleted from outdir if present (removes obsolete files)
if [ -z "$1" ] || [ -z "$2" ]
  then
   echo "usage:  sh generate_orig.sh <dict> <parent-dir>"
   echo "Example: sh generate_orig.sh acc tempparent/acc"
   echo "Example: sh generate_orig.sh acc ../../ACCScan/2020"
   exit 1
  else
    dict=$1  # assume this is lowercase
    outdir=$2
fi

 python3 generate.py "$dict" inventory.txt  makotemplates distinctfiles/${dict} $outdir
