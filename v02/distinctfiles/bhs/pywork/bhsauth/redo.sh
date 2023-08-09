echo "bhsauthtooltips.sqlite"
sqlite3 bhsauthtooltips.sqlite < tooltips.sql
chmod 0755 bhsauthtooltips.sqlite  # needed?
echo "move bhsauthtooltips.sqlite to web/sqlite"
mv bhsauthtooltips.sqlite ../../web/sqlite/
