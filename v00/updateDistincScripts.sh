#!/bin/bash
echo "Download unique scripts to each dictionary's pywork from live Cologne server to distinctscripts folder."
scripts=(make_xml.py)
dictsthirteen=(BUR INM MWE PWG SKD STC VCP)
dictsfourteen=(ACC AE AP90 AP BEN BHS BOP BOR CAE CCS GRA GST IEG KRM MCI MD MW72 MW PD PE PGN PUI PW SCH SHS SNP VEI WIL YAT)
for dict in ${dictsthirteen[*]}
do
	for script in ${scripts[*]}
	do
		wget -O distinctscripts/"$dict"Scan/2020/pywork/make_xml.py https://www.sanskrit-lexicon.uni-koeln.de/scans/"$dict"Scan/2013/pywork/make_xml.py
	done
	wget -O distinctscripts/"$dict"Scan/2020/pywork/${dict,,}.dtd https://www.sanskrit-lexicon.uni-koeln.de/scans/"$dict"Scan/2013/pywork/${dict,,}.dtd
done

for dict in ${dictsfourteen[*]}
do
	for script in ${scripts[*]}
	do
		wget -O distinctscripts/"$dict"Scan/2020/pywork/make_xml.py https://www.sanskrit-lexicon.uni-koeln.de/scans/"$dict"Scan/2014/pywork/make_xml.py
	done
	wget -O distinctscripts/"$dict"Scan/2020/pywork/${dict,,}.dtd https://www.sanskrit-lexicon.uni-koeln.de/scans/"$dict"Scan/2014/pywork/${dict,,}.dtd
done

