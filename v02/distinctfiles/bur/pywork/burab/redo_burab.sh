echo "remaking burab.sqlite"
rm burab.sqlite
python3 ../sqlite/sqlite_txt.py burab_input.txt burab.sqlite burab
echo "finished remaking burab.sqlite"
chmod 0755 burab.sqlite
