echo "remaking pwgbib.sqlite"
rm pwgbib.sqlite
python3 ../sqlite/sqlite_txt.py pwgbib_input.txt pwgbib.sqlite pwgbib
echo "finished remaking pwgbib.sqlite"
chmod 0755 pwgbib.sqlite
