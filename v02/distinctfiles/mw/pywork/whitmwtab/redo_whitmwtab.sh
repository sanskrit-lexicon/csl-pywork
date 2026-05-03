echo "remaking whitmwtab.sqlite"
rm whitmwtab.sqlite
python3 ../sqlite/sqlite_txt.py whitmwtab_input.txt whitmwtab.sqlite whitmwtab
echo "finished remaking whitmwtab.sqlite"
chmod 0755 whitmwtab.sqlite
