echo "tooltip.txt ..."
#python tooltip.py roman mwauth.txt tooltip.txt
#echo "temp_tooltip.txt ..."
#python temp_tooltip.py roman mwauth.txt temp_tooltip.txt
echo "mwauthtooltips.sqlite"
rm -f mwauthtooltips.sqlite
python3 ../sqlite/sqlite_txt.py tooltip.txt mwauthtooltips.sqlite mwauthtooltips
chmod 0755 mwauthtooltips.sqlite  # needed?
echo "copy mwauthtooltips.sqlite to web/sqlite"
cp mwauthtooltips.sqlite ../../web/sqlite/
