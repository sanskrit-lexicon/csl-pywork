echo "benauthtooltips.sqlite"
sqlite3 benauthtooltips.sqlite < tooltips.sql
chmod 0755 benauthtooltips.sqlite  # needed?
echo "move benauthtooltips.sqlite to web/sqlite"
mv benauthtooltips.sqlite ../../web/sqlite/
