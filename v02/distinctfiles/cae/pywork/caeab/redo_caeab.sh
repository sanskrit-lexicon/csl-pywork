echo "remaking caeab.sqlite"
rm caeab.sqlite
sqlite3 caeab.sqlite < caeab.sql
echo "finished remaking caeab.sqlite"
chmod 0755 caeab.sqlite
