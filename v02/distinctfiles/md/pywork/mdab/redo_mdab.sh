echo "remaking mdab.sqlite"
rm mdab.sqlite
python3 ../sqlite/sqlite_txt.py mdab_input.txt mdab.sqlite mdab
echo "finished remaking mdab.sqlite"
chmod 0755 mdab.sqlite
