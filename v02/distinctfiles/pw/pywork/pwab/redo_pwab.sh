echo "remaking pwab.sqlite"
rm pwab.sqlite
sqlite3 pwab.sqlite < pwab.sql
echo "finished remaking pwab.sqlite"
chmod 0755 pwab.sqlite
