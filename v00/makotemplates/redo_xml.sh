echo "BEGIN redo_xml.sh"
echo "construct gra.xml..."
python make_xml.py ../orig/${dictlo}.txt ${dictlo}hw.txt ${dictlo}.xml # > redoxml_log.txt
echo "xmllint on gra.xml..."
xmllint --noout --valid ${dictlo}.xml
echo "gra.sqlite..."
cd ../web/sqlite
sh redo.sh
echo "query_dump ..."
cd ../webtc2
sh init_query.sh
echo "END redo_xml.sh"
