echo "schauthtooltips.sqlite"
rm -f schauthtooltips.sqlite
python3 ../sqlite/sqlite_txt.py tooltip.txt schauthtooltips.sqlite schauthtooltips
chmod 0755 schauthtooltips.sqlite  # needed?
echo "copy schauthtooltips.sqlite to web/sqlite"
cp schauthtooltips.sqlite ../../web/sqlite/
