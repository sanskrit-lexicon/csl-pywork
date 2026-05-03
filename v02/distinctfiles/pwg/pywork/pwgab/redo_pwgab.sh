echo "remaking pwgab.sqlite"
rm pwgab.sqlite
python3 ../sqlite/sqlite_txt.py pwgab_input.txt pwgab.sqlite pwgab
echo "finished remaking pwgab.sqlite"
chmod 0755 pwgab.sqlite
