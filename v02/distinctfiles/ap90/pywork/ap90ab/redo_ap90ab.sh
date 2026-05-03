echo "remaking ap90ab.sqlite"
rm ap90ab.sqlite
python3 ../sqlite/sqlite_txt.py ap90ab_input.txt ap90ab.sqlite ap90ab
echo "finished remaking ap90ab.sqlite"
chmod 0755 ap90ab.sqlite
