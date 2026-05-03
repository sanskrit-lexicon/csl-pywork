echo "BEGIN redo_xml.sh"

echo "construct ${dictlo}.xml..."
echo "BEGIN make_xml.py"
%if cologne_flag:
python3 make_xml.py ../orig/${dictlo}.txt ${dictlo}hw.txt ${dictlo}.xml # > redoxml_log.txt
%else:
python3 make_xml.py ../orig/${dictlo}.txt ${dictlo}hw.txt ${dictlo}.xml # > redoxml_log.txt
%endif
echo "END make_xml.py"
echo "xmllint on ${dictlo}.xml..."
xmlint_err=$(xmllint --noout --valid ${dictlo}.xml 2>&1)
if [ -n "$xmlint_err" ]; then
  echo "BEGIN xmllint_err"
  echo "$xmlint_err"
  echo "END xmllint_err"
fi
echo "${dictlo}.sqlite..."
#  construct things that depend on xxx.xml
sh redo_postxml.sh
echo "END redo_xml.sh"
