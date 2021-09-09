echo "remaking benab.sqlite"
rm benab.sqlite
sqlite3 benab.sqlite < benab.sql
echo "finished remaking benab.sqlite"
chmod 0755 benab.sqlite
