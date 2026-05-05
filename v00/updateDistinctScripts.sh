#!/bin/bash
# updateDistinctScripts.sh
# Downloads per-dictionary xxx.dtd files from the live Cologne server into
# the local distinctscripts/ directory.
#
# Usage: sh updateDistinctScripts.sh
#   (no arguments; updates all dictionaries)
#
# Sources DTD files from XXXScan/2013/ (BUR INM MWE PWG SKD STC VCP)
# or XXXScan/2014/ (all other dictionaries) on the Cologne server.
# The make_xml.py download lines are currently commented out.
#
# Prerequisites: wget, network access to www.sanskrit-lexicon.uni-koeln.de.
# Note: v00 is superseded by v02, which templates xxx.dtd rather than
# downloading it.

echo "Download unique scripts to each dictionary's pywork from live Cologne server to distinctscripts folder."
scripts=(make_xml.py)
dictsthirteen=(BUR INM MWE PWG SKD STC VCP)
dictsfourteen=(ACC AE AP90 AP BEN BHS BOP BOR CAE CCS GRA GST IEG KRM MCI MD MW72 MW PD PE PGN PUI PW SCH SHS SNP VEI WIL YAT)
for dict in ${dictsthirteen[*]}
do
	for script in ${scripts[*]}
	do
		#wget -O distinctscripts/"$dict"Scan/2020/pywork/make_xml.py https://www.sanskrit-lexicon.uni-koeln.de/scans/"$dict"Scan/2013/pywork/make_xml.py
	done
	wget -O distinctscripts/"$dict"Scan/2020/pywork/$(echo "$dict" | tr '[:upper:]' '[:lower:]').dtd https://www.sanskrit-lexicon.uni-koeln.de/scans/"$dict"Scan/2013/pywork/$(echo "$dict" | tr '[:upper:]' '[:lower:]').dtd
done

for dict in ${dictsfourteen[*]}
do
	for script in ${scripts[*]}
	do
		#wget -O distinctscripts/"$dict"Scan/2020/pywork/make_xml.py https://www.sanskrit-lexicon.uni-koeln.de/scans/"$dict"Scan/2014/pywork/make_xml.py
	done
	wget -O distinctscripts/"$dict"Scan/2020/pywork/$(echo "$dict" | tr '[:upper:]' '[:lower:]').dtd https://www.sanskrit-lexicon.uni-koeln.de/scans/"$dict"Scan/2014/pywork/$(echo "$dict" | tr '[:upper:]' '[:lower:]').dtd
done

