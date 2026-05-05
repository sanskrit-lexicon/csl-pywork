#!/bin/bash
# compare.sh
# Diffs generated pywork scripts against a local Cologne server copy to spot
# unintended changes after a regeneration.
#
# Usage: sh compare.sh
#   (no arguments; edit the 'scripts' array to choose which files to compare)
#
# Compares: ../../../Cologne_localcopy/<dict>/pywork/<script>
#      vs:  ../../<DICT>Scan/2020/pywork/<script>
#
# Prerequisites: a local Cologne copy must exist at ../../../Cologne_localcopy/.
# Currently checks: hw2.py

scripts=(hw2.py)
dicts=(BUR INM MWE PWG SKD STC VCP ACC AE AP90 AP BEN BHS BOP BOR CAE CCS GRA GST IEG KRM MCI MD MW72 MW PD PE PGN PUI PW SCH SHS SNP VEI WIL YAT)
for dict in ${dicts[*]}
do
	echo $dict
	for script in ${scripts[*]}
	do
		diff ../../../Cologne_localcopy/"$(echo "$dict" | tr '[:upper:]' '[:lower:]')"/pywork/"$script" ../../"$dict"Scan/2020/pywork/"$script"
	done
done

