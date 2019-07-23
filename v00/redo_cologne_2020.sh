#!/bin/bash
echo "Generate the code from template for each dictionary."
dicts=(ACC AE AP90 AP BEN BHS BOP BOR BUR CAE CCS GRA GST IEG INM KRM MCI MD MW72 MWE MW PD PE PGN PUI PWG PW SCH SHS SKD SNP STC VCP VEI WIL YAT)
for dict in ${dicts[*]}
do
	python generate.py "$dict" inventory.txt  makotemplates ../../"$dict"Scan/2020/pywork
done
echo "Copying the make_xml.py to respective dictionaries."
cp -r distinctscripts/* ../..
