#!/bin/bash
# generate_orig.sh
# Copies source digitisation files from csl-orig into the target directory.
#
# Usage: sh generate_orig.sh <dict> <outdir>
#   <dict>    lowercase dictionary code (e.g. mw, skd)
#   <outdir>  target directory (e.g. ../../MWScan/2020 or tempparent/mw)
#
# Reads inventory_orig.txt to determine which files to copy, then runs
# generate.py against csl-orig/v02/<dict>/ as the source.
# Populates outdir/orig/ (xxx.txt) and outdir/pywork/ (hwextra, header, meta files).
if [ -z "$1" ] || [ -z "$2" ]
  then
   echo "usage:  sh generate_orig.sh <dict> <parent-dir>"
   echo "Example: sh generate_orig.sh acc tempparent/acc"
   echo "Example: sh generate_orig.sh acc ../../ACCScan/2020"
   exit 1
  else
    dict=$(echo "$1" | tr '[:lower:]' '[:upper:]') # Uppercase
    outdir=$2
fi

dictlo=$(echo "$dict" | tr '[:upper:]' '[:lower:]') # Lowercase
dictup=$dict

#python generate.py "$dict" inventory_orig.txt _ '../../csl-orig/v00/csl-data/${dictup}Scan/2020' $outdir

python3 generate.py "$dict" inventory_orig.txt _ '../../csl-orig/v02/${dictlo}' $outdir

