echo "benauthtooltips.sqlite"
rm -f benauthtooltips.sqlite
python3 ../sqlite/sqlite_txt.py tooltip.txt benauthtooltips.sqlite benauthtooltips
chmod 0755 benauthtooltips.sqlite  # needed?
echo "move benauthtooltips.sqlite to web/sqlite"
mv benauthtooltips.sqlite ../../web/sqlite/
