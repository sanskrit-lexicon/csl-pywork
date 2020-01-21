echo "remaking stcab.sqlite"
rm stcab.sqlite
sqlite3 stcab.sqlite < stcab.sql
echo "finished remaking stcab.sqlite"
chmod 0755 stcab.sqlite
