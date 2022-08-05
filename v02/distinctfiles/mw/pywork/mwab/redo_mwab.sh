echo "checking mwab_input.txt..."
python check.py 2 mwab_input.txt
echo "remaking mwab.sqlite"
rm mwab.sqlite
sqlite3 mwab.sqlite < mwab.sql
echo "finished remaking mwab.sqlite"
chmod 0755 mwab.sqlite
