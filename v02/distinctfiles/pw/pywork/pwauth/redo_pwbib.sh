echo "remaking pwbib.sqlite"
rm pwbib.sqlite
sqlite3 pwbib.sqlite < pwbib.sql
echo "finished remaking pwbib.sqlite"
chmod 0755 pwbib.sqlite
