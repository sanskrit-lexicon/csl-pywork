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
xmllint_err=$(xmllint --noout --valid ${dictlo}.xml 2>&1)
xmllint_status=$?
if [ -n "$xmllint_err" ]; then
  echo "BEGIN xmllint_err"
  echo "$xmllint_err"
  echo "END xmllint_err"
fi
# if xmllint is not installed, set xmllint_status to 0
# and proceed with rest of script.
# This is done so that local xammp installation in Windows 
# with git-bash terminal can proceed.
# In this case, xmllint is not available as a command,
# and a separate python program in local installation
# is responsible to check xml validity.
if command -v xmllint >/dev/null 2>&1; then
 echo "xmllint is installed."
else
    echo "xmllint is not installed or not in PATH."
    echo "PROCEDING with redo_xml.sh"
 # reset xmllint_status to 0
 xmllint_status=0
fi

# fail-closed: do not build sqlite/query_dump/downloads from an invalid XML
if [ $make_xml_status -ne 0 ] || [ $xmllint_status -ne 0 ]; then
  printf "\033[31mSTOP redo_xml.sh: make_xml.py status %s, xmllint status %s — redo_postxml.sh NOT run\033[0m\n" "$make_xml_status" "$xmllint_status"
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
