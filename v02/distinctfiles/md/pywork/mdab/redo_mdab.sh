echo "remaking mdab.sqlite"
rm mdab.sqlite
sqlite3 mdab.sqlite < mdab.sql
echo "finished remaking mdab.sqlite"
chmod 0755 mdab.sqlite
