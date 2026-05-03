echo "remaking pwab.sqlite"
rm pwab.sqlite
python3 ../sqlite/sqlite_txt.py pwab_input.txt pwab.sqlite pwab
echo "finished remaking pwab.sqlite"
chmod 0755 pwab.sqlite
