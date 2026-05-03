echo "remaking caeab.sqlite"
rm caeab.sqlite
python3 ../sqlite/sqlite_txt.py caeab_input.txt caeab.sqlite caeab
echo "finished remaking caeab.sqlite"
chmod 0755 caeab.sqlite
