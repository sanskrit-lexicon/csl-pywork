echo "remaking westmwtab.sqlite"
rm westmwtab.sqlite
sqlite3 westmwtab.sqlite < westmwtab.sql
echo "finished remaking westmwtab.sqlite"
chmod 0755 westmwtab.sqlite
