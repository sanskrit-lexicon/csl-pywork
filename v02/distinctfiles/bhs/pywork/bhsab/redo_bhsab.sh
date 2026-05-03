echo "remaking bhsab.sqlite"
rm bhsab.sqlite
python3 ../sqlite/sqlite_txt.py bhsab_input.txt bhsab.sqlite bhsab
echo "finished remaking bhsab.sqlite"
chmod 0755 bhsab.sqlite
