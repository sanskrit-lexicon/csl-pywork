#!/bin/bash
# cologne_test.sh
# Checks that a freshly generated xxx.xml matches the original Cologne server XML.
#
# Usage: sh cologne_test.sh <dict> <outdir>
#   <dict>    lowercase dictionary code (e.g. mw, skd)
#   <outdir>  the output directory used when generate_dict.sh was run
#             (e.g. ../../MWScan/2020)
#
# The "original" XML is taken from the Cologne server layout:
#   XXXScan/2013/pywork/xxx.xml  for BUR INM MWE PWG SKD STC VCP
#   XXXScan/2014/pywork/xxx.xml  for all other dictionaries
#
# Output: diff written to temp_xmldiffs/diff_xml_<dict>.txt
#         line count of the diff printed to stdout (0 = identical)
#
# Prerequisites: temp_xmldiffs/ directory must exist before running.

dictlo="$1"
outdir="$2"
pwd
# ---------------------------------------------------------
# part 2: test that xxx.xml is same as the original one in XXXScan/2013(4)

dictsthirteen=(BUR INM MWE PWG SKD STC VCP)
dictsfourteen=(ACC AE AP90 AP BEN BHS BOP BOR CAE CCS GRA GST IEG KRM MCI MD MW72 MW PD PE PGN PUI PW SCH SHS SNP VEI WIL YAT)
dictup=$(echo "$dictlo" | tr '[:lower:]' '[:upper:]')

# inefficient, but who cares?
dictyear="0"
for dict in ${dictsthirteen[*]}
do
 #echo "dict=$dict, dictup=$dictup"
 if [ $dictup == $dict ]
  then
   dictyear="2013"
   break
 fi
done

for dict in ${dictsfourteen[*]}
do
 #echo "dict=$dict, dictup=$dictup"
 if [ $dictup == $dict ]
  then
   dictyear="2014"
   break
 fi
done
## now we have dictyear
dictup=$(echo "$dictlo" | tr '[:lower:]' '[:upper:]')
olddir="../../${dictup}Scan/$dictyear"
oldxml="$olddir/pywork/$dictlo.xml"
newdir="$outdir"
newxml="$newdir/pywork/$dictlo.xml"
echo "checking 'diff $oldxml $newxml'"
diffout="temp_xmldiffs/diff_xml_${dictlo}.txt"
diff $oldxml $newxml > $diffout
wc -l $diffout
