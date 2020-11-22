echo "remaking lanab.sqlite"
rm lanab.sqlite
sqlite3 lanab.sqlite < lanab.sql
echo "finished remaking lanab.sqlite"
chmod 0755 lanab.sqlite
