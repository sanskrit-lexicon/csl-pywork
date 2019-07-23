#!/bin/bash
echo "Regenerate the headwords, xml and sqlites for specified dictionaries."
echo "Usage - ./redo.sh [dictcode]."
echo "If dictcode is not specified, all the dictionaries are updated and regenerated."

if [ -z "$1" ]
then
dicts=(${$1^^}) # Uppercase
else
dicts=(BUR INM MWE PWG SKD STC VCP ACC AE AP90 AP BEN BHS BOP BOR CAE CCS GRA GST IEG KRM MCI MD MW72 MW PD PE PGN PUI PW SCH SHS SNP VEI WIL YAT)
fi
echo "UPDATING THE FOLLOWING DICTIONARIES."
echo $dicts

# Go to scans folder
cd ..
echo "STEP 1. UPDATE THE WEB DISPLAY CODE BASE FROM GITHUB."
cd csl-websanlexicon/v00
git pull origin master
bash redo_cologne_2020.sh
echo "STEP 2. UPDATE THE PYWORK CODE BASE FROM GITHUB."
cd ../../csl-pywork/v00
git pull origin master
bash redo_cologne_2020.sh
echo "STEP 3. UPDATE THE DICTIONARY TEXT FILES FROM GITHUB."
cd ../../csl-orig/v00
git pull origin master
bash redo_cologne_2020.sh
echo ""
echo ""

cd ../..
for dict in ${dicts[*]}
do
	echo $dict
	# ${dict,,} stands for lowercase.
	echo "STEP 4. REGENERATION FOR  $dict"
	cd "$dict"Scan/2020/pywork/
	echo "STEP 4A. REGENERATING HEADWORDS FOR $dict"
	sh redo_hw.sh
	echo "STEP 4B. REGENERATING XML AND SQLITE FOR $dict"
	sh redo_xml.sh
	echo "COMPLETED REGENERATION FOR $dict"
	cd ../../..
	echo ""
	echo ""
done

cd csl-pywork

