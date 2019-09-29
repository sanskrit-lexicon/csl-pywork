echo "remaking pwgbib.sqlite"
rm pwgbib.sqlite
sqlite3 pwgbib.sqlite < pwgbib.sql
echo "finished remaking pwgbib.sqlite"
chmod 0755 pwgbib.sqlite
