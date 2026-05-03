echo "checking mwab_input.txt..."
python3 check.py 2 mwab_input.txt
echo "remaking mwab.sqlite"
rm mwab.sqlite
python3 ../sqlite/sqlite_txt.py mwab_input.txt mwab.sqlite mwab
echo "finished remaking mwab.sqlite"
chmod 0755 mwab.sqlite
