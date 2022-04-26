echo "remaking pwkvnab.sqlite"
rm pwkvnab.sqlite
sqlite3 pwkvnab.sqlite < pwkvnab.sql
echo "finished remaking pwkvnab.sqlite"
chmod 0755 pwkvnab.sqlite
