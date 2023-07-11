echo "graauthtooltips.sqlite"
sqlite3 graauthtooltips.sqlite < tooltips.sql
chmod 0755 graauthtooltips.sqlite  # needed?
echo "move graauthtooltips.sqlite to web/sqlite"
mv graauthtooltips.sqlite ../../web/sqlite/
