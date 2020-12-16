echo "remaking input.txt..."
php make_input.php ../${dictlo}.xml input.txt
sqlitedb="${dictlo}.sqlite"
if [ -f "$sqlitedb" ]
 then
  rm  $sqlitedb
fi
echo "remaking sqlite table..."
sqlite3 $sqlitedb < def.sql
echo "moving $sqlitedb to web/sqlite/"
# remove input.txt  -- not needed once prior step loads inti $sqlitedb
rm input.txt
# assume ../../web/sqlite directory exists
# assume directory containing this redo.sh file is subdirectory of pywork
# and that pywork is sibling directory of pywork
mv ${dictlo}.sqlite ../../web/sqlite/
