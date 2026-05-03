echo "remaking pwbib.sqlite"
rm pwbib.sqlite
python3 ../sqlite/sqlite_txt.py pwbib_input.txt pwbib.sqlite pwbib
echo "finished remaking pwbib.sqlite"
chmod 0755 pwbib.sqlite
