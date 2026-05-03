echo "remaking stcab.sqlite"
rm stcab.sqlite
python3 ../sqlite/sqlite_txt.py stcab_input.txt stcab.sqlite stcab
echo "finished remaking stcab.sqlite"
chmod 0755 stcab.sqlite
