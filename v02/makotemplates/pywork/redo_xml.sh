unset CDPATH
echo "BEGIN redo_xml.sh"

echo "construct ${dictlo}.xml..."
echo "BEGIN make_xml.py"
%if cologne_flag:
python3 make_xml.py ../orig/${dictlo}.txt ${dictlo}hw.txt ${dictlo}.xml # > redoxml_log.txt
%else:
python3 make_xml.py ../orig/${dictlo}.txt ${dictlo}hw.txt ${dictlo}.xml # > redoxml_log.txt
%endif
make_xml_status=$?
echo "END make_xml.py"
echo "xmllint on ${dictlo}.xml..."
xmlint_err=$(xmllint --noout --valid ${dictlo}.xml 2>&1)
xmlint_status=$?
if [ -n "$xmlint_err" ]; then
  echo "BEGIN xmllint_err"
  echo "$xmlint_err"
  echo "END xmllint_err"
fi
# fail-closed: do not build sqlite/query_dump/downloads from an invalid XML
if [ $make_xml_status -ne 0 ] || [ $xmlint_status -ne 0 ]; then
  printf "\033[31mSTOP redo_xml.sh: make_xml.py status %s, xmllint status %s — redo_postxml.sh NOT run\033[0m\n" "$make_xml_status" "$xmlint_status"
  exit 1
fi
echo "${dictlo}.sqlite..."
#  construct things that depend on xxx.xml
sh redo_postxml.sh
redo_postxml_status=$?
if [ $redo_postxml_status -ne 0 ]; then
  printf "\033[31mSTOP redo_xml.sh: redo_postxml.sh status %s\033[0m\n" "$redo_postxml_status"
  exit 1
fi
echo "END redo_xml.sh"
