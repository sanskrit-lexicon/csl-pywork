echo "ap90authtooltips.sqlite"
sqlite3 ap90authtooltips.sqlite < tooltips.sql
chmod 0755 ap90authtooltips.sqlite  # needed?
echo "copy ap90authtooltips.sqlite to web/sqlite"
cp ap90authtooltips.sqlite ../../web/sqlite/
