echo "remaking ap90ab.sqlite"
rm ap90ab.sqlite
sqlite3 ap90ab.sqlite < ap90ab.sql
echo "finished remaking ap90ab.sqlite"
chmod 0755 ap90ab.sqlite
