#!/bin/bash
# Regenerate the headwords, xml and sqlites for specified dictionaries.
# Usage - bash redo.sh [dictcode].
# If dictcode is not specified, all the dictionaries are updated and regenerated.

if [ -z "$1" ]
  then
	dicts=(BUR INM MWE PWG SKD STC VCP ACC AE AP90 AP BEN BHS BOP BOR CAE CCS GRA GST IEG KRM MCI MD MW72 MW PD PE PGN PUI PW SCH SHS SNP VEI WIL YAT)
  else
    dicts=(${1^^}) # Uppercase
fi

# Go to scans folder
cd ..
echo "INFO - STEP 1. UPDATE THE WEB DISPLAY CODE BASE FROM GITHUB."
cd csl-websanlexicon/v00
git pull origin master
if [ -z "$1" ]
  then
  bash redo_cologne_2020.sh
  else
  bash redo_cologne_2020.sh $1
fi
echo ""
echo ""
echo "INFO - STEP 2. UPDATE THE PYWORK CODE BASE FROM GITHUB."
cd ../../csl-pywork/v00
git pull origin master
if [ -z "$1" ]
  then
  bash redo_cologne_2020.sh
  else
  bash redo_cologne_2020.sh $1
fi
echo ""
echo ""
echo "INFO - STEP 3. UPDATE THE DICTIONARY TEXT FILES FROM GITHUB."
cd ../../csl-orig/v00
git pull origin master
cd ../..
echo ""
echo ""

echo "INFO - UPDATING THE FOLLOWING DICTIONARIES."
echo "${dicts[*]}"
echo ""
echo ""

for dict in ${dicts[*]}
do
	# ${dict,,} stands for lowercase.
	echo "INFO - STEP 4. REGENERATION FOR $dict"
	echo ""
	cd "$dict"Scan/2020/pywork/
	echo "INFO - STEP 4A. REGENERATING HEADWORDS FOR $dict"
	sh redo_hw.sh
	echo ""
	echo "INFO - STEP 4B. REGENERATING XML AND SQLITE FOR $dict"
	sh redo_xml.sh
	echo ""
	echo "INFO - STEP 4C. COMPLETED REGENERATION FOR $dict"
	cd ../../..
	echo ""
	echo ""
done

cd csl-pywork

