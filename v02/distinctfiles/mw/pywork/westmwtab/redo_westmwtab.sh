echo "remaking westmwtab.sqlite"
rm westmwtab.sqlite
python3 ../sqlite/sqlite_txt.py westmwtab_input.txt westmwtab.sqlite westmwtab
echo "finished remaking westmwtab.sqlite"
chmod 0755 westmwtab.sqlite
