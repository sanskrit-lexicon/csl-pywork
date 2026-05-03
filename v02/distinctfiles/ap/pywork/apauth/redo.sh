echo "apauthtooltips.sqlite"
rm -f apauthtooltips.sqlite
python3 ../sqlite/sqlite_txt.py tooltip.txt apauthtooltips.sqlite apauthtooltips
chmod 0755 apauthtooltips.sqlite  # needed?
echo "copy apauthtooltips.sqlite to web/sqlite"
cp apauthtooltips.sqlite ../../web/sqlite/
