echo "remaking lanab.sqlite"
rm lanab.sqlite
python3 ../sqlite/sqlite_txt.py lanab_input.txt lanab.sqlite lanab
echo "finished remaking lanab.sqlite"
chmod 0755 lanab.sqlite
