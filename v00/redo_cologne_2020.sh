#!/bin/bash
# redo_cologne_2020.sh
# Regenerates pywork scripts for one or all dictionaries using the v00 pipeline.
#
# Usage: bash redo_cologne_2020.sh [DICTCODE]
#   (no args)   regenerate all dictionaries
#   DICTCODE    regenerate a single dictionary (case-insensitive, e.g. MW or mw)
#
# Two-step process:
#   1. Runs generate.py with inventory.txt and makotemplates/ to populate
#      ../../<DICT>Scan/2020/pywork/ with shared/templated scripts.
#   2. Copies the per-dictionary make_xml.py and xxx.dtd from distinctscripts/
#      into the target pywork/ directory (the v00 equivalent of the CD category).
#
# Note: v00 is superseded by v02. Use v02/generate_dict.sh for current work.
if [ -z "$1" ]
  then
	dicts=(BUR INM MWE PWG SKD STC VCP ACC AE AP90 AP BEN BHS BOP BOR CAE CCS GRA GST IEG KRM MCI MD MW72 MW PD PE PGN PUI PW SCH SHS SNP VEI WIL YAT)
  else
    dicts=($(echo "$1" | tr '[:lower:]' '[:upper:]')) # Uppercase
fi

echo "Generating the pywork code from templates for the dictionaries."
for dict in ${dicts[*]}
do
	python generate.py "$dict" inventory.txt  makotemplates ../../"$dict"Scan/2020/pywork
done
echo "Copying the unique make_xml.py and xxx.dtd to respective dictionaries."
if [ -z "$1" ]
  then
  cp -r distinctscripts/* ../..
  else
  cp -r distinctscripts/$(echo "$1" | tr '[:lower:]' '[:upper:]')Scan/* ../../$(echo "$1" | tr '[:lower:]' '[:upper:]')Scan
fi

