echo "remaking mwkeys.sqlite"
rm mwkeys.sqlite
sqlite3 mwkeys.sqlite < mwkeys.sql
echo "finished remaking mwkeys.sqlite"
chmod 0755 mwkeys.sqlite
