echo "remaking pwkvnbib.sqlite"
rm pwkvnbib.sqlite
sqlite3 pwkvnbib.sqlite < pwkvnbib.sql
echo "finished remaking pwkvnbib.sqlite"
chmod 0755 pwkvnbib.sqlite
