echo "remaking pwgab.sqlite"
rm pwgab.sqlite
sqlite3 pwgab.sqlite < pwgab.sql
echo "finished remaking pwgab.sqlite"
chmod 0755 pwgab.sqlite
