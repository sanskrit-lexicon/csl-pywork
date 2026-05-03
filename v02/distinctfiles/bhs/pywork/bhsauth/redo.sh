echo "bhsauthtooltips.sqlite"
rm -f bhsauthtooltips.sqlite
python3 ../sqlite/sqlite_txt.py tooltip.txt bhsauthtooltips.sqlite bhsauthtooltips
chmod 0755 bhsauthtooltips.sqlite  # needed?
echo "move bhsauthtooltips.sqlite to web/sqlite"
mv bhsauthtooltips.sqlite ../../web/sqlite/
