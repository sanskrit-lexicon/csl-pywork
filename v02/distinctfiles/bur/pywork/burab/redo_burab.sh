echo "remaking burab.sqlite"
rm burab.sqlite
sqlite3 burab.sqlite < burab.sql
echo "finished remaking burab.sqlite"
chmod 0755 burab.sqlite
