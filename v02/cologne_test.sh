dictlo="$1"
outdir="$2"
pwd
# ---------------------------------------------------------
# part 2: test that xxx.xml is same as the original one in XXXScan/2013(4)

dictsthirteen=(BUR INM MWE PWG SKD STC VCP)
dictsfourteen=(ACC AE AP90 AP BEN BHS BOP BOR CAE CCS GRA GST IEG KRM MCI MD MW72 MW PD PE PGN PUI PW SCH SHS SNP VEI WIL YAT)
dictup="${dictlo^^}"

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
dictup="${dictlo^^}"
olddir="../../${dictup}Scan/$dictyear"
oldxml="$olddir/pywork/$dictlo.xml"
newdir="$outdir"
newxml="$newdir/pywork/$dictlo.xml"
echo "checking 'diff $oldxml $newxml'"
diffout="temp_xmldiffs/diff_xml_${dictlo}.txt"
diff $oldxml $newxml > $diffout
wc -l $diffout
