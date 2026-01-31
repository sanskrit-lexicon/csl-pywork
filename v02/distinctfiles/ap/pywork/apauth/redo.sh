echo "apauthtooltips.sqlite"
sqlite3 apauthtooltips.sqlite < tooltips.sql
chmod 0755 apauthtooltips.sqlite  # needed?
echo "copy apauthtooltips.sqlite to web/sqlite"
cp apauthtooltips.sqlite ../../web/sqlite/
