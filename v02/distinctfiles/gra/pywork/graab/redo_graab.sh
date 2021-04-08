echo "remaking graab.sqlite"
rm graab.sqlite
sqlite3 graab.sqlite < graab.sql
echo "finished remaking graab.sqlite"
chmod 0755 graab.sqlite
