echo "remaking pwkvnab.sqlite"
rm pwkvnab.sqlite
python3 ../sqlite/sqlite_txt.py pwkvnab_input.txt pwkvnab.sqlite pwkvnab
echo "finished remaking pwkvnab.sqlite"
chmod 0755 pwkvnab.sqlite
