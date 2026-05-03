echo "remaking graab.sqlite"
rm graab.sqlite
python3 ../sqlite/sqlite_txt.py graab_input.txt graab.sqlite graab
echo "finished remaking graab.sqlite"
chmod 0755 graab.sqlite
