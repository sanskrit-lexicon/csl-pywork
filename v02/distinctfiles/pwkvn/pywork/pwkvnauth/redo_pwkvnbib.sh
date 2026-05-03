echo "remaking pwkvnbib.sqlite"
rm pwkvnbib.sqlite
python3 ../sqlite/sqlite_txt.py pwkvnbib_input.txt pwkvnbib.sqlite pwkvnbib
echo "finished remaking pwkvnbib.sqlite"
chmod 0755 pwkvnbib.sqlite
