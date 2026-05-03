echo "remaking benab.sqlite"
rm benab.sqlite
python3 ../sqlite/sqlite_txt.py benab_input.txt benab.sqlite benab
echo "finished remaking benab.sqlite"
chmod 0755 benab.sqlite
