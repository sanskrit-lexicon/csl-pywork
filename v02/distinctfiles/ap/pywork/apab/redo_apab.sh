echo "remaking apab.sqlite"
rm apab.sqlite
sqlite3 apab.sqlite < apab.sql
echo "finished remaking apab.sqlite"
chmod 0755 apab.sqlite
