echo "schauthtooltips.sqlite"
sqlite3 schauthtooltips.sqlite < tooltips.sql
chmod 0755 schauthtooltips.sqlite  # needed?
echo "copy schauthtooltips.sqlite to web/sqlite"
cp schauthtooltips.sqlite ../../web/sqlite/
