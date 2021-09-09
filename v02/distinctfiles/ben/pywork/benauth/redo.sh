echo "benauthtooltips.sqlite"
sqlite3 benauthtooltips.sqlite < tooltips.sql
chmod 0755 benauthtooltips.sqlite  # needed?
echo "copy benauthtooltips.sqlite to web/sqlite"
cp benauthtooltips.sqlite ../../web/sqlite/
