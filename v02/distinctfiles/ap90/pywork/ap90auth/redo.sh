echo "ap90authtooltips.sqlite"
rm -f ap90authtooltips.sqlite
python3 ../sqlite/sqlite_txt.py tooltip.txt ap90authtooltips.sqlite ap90authtooltips
chmod 0755 ap90authtooltips.sqlite  # needed?
echo "copy ap90authtooltips.sqlite to web/sqlite"
cp ap90authtooltips.sqlite ../../web/sqlite/
