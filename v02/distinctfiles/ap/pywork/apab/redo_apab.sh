echo "remaking apab.sqlite"
rm apab.sqlite
python3 ../sqlite/sqlite_txt.py apab_input.txt apab.sqlite apab
echo "finished remaking apab.sqlite"
chmod 0755 apab.sqlite
