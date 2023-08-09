echo "remaking bhsab.sqlite"
rm bhsab.sqlite
sqlite3 bhsab.sqlite < bhsab.sql
echo "finished remaking bhsab.sqlite"
chmod 0755 bhsab.sqlite
