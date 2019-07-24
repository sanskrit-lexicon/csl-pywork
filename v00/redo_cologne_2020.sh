#!/bin/bash
# Regenerate the pywork code for specified dictionaries.
# Usage - bash redo_cologne_2020.sh [dictcode].
# If dictcode is not specified, pywork of all the dictionaries are updated.
if [ -z "$1" ]
  then
	dicts=(BUR INM MWE PWG SKD STC VCP ACC AE AP90 AP BEN BHS BOP BOR CAE CCS GRA GST IEG KRM MCI MD MW72 MW PD PE PGN PUI PW SCH SHS SNP VEI WIL YAT)
  else
    dicts=(${1^^}) # Uppercase
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
  cp -r distinctscripts/${1^^}Scan/* ../../${1^^}Scan
fi

