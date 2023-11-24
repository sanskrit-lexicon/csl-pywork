echo "BEGIN redo_xml.sh"

echo "construct ${dictlo}.xml..."
%if cologne_flag:
python3 make_xml.py ../orig/${dictlo}.txt ${dictlo}hw.txt ${dictlo}.xml # > redoxml_log.txt
%else:
python3 make_xml.py ../orig/${dictlo}.txt ${dictlo}hw.txt ${dictlo}.xml # > redoxml_log.txt
%endif
echo "xmllint on ${dictlo}.xml..."
xmllint --noout --valid ${dictlo}.xml
echo "${dictlo}.sqlite..."
#  construct things that depend on xxx.xml
sh redo_postxml.sh
echo "END redo_xml.sh"
