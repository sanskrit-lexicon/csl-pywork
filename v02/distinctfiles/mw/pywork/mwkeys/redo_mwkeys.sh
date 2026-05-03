echo "remaking mwkeys.sqlite"
rm mwkeys.sqlite
python3 ../sqlite/sqlite_txt.py extract_keys_b.txt mwkeys.sqlite mwkeys
echo "finished remaking mwkeys.sqlite"
chmod 0755 mwkeys.sqlite
