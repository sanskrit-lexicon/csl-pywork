echo "graauthtooltips.sqlite"
rm -f graauthtooltips.sqlite
python3 ../sqlite/sqlite_txt.py tooltip.txt graauthtooltips.sqlite graauthtooltips
chmod 0755 graauthtooltips.sqlite  # needed?
echo "move graauthtooltips.sqlite to web/sqlite"
mv graauthtooltips.sqlite ../../web/sqlite/
