sqlitedb="${dictlo}.sqlite"
xml="../${dictlo}.xml"
echo "remaking $sqlitedb from $xml with python..."
python sqlite.py $xml $sqlitedb
echo "moving $sqlitedb to web/sqlite/"
mv ${dictlo}.sqlite ../../web/sqlite/
