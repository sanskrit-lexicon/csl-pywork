echo "remaking whitmwtab.sqlite"
rm whitmwtab.sqlite
sqlite3 whitmwtab.sqlite < whitmwtab.sql
echo "finished remaking whitmwtab.sqlite"
chmod 0755 whitmwtab.sqlite
