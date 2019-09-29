echo "BEGIN: downloads/redo_xml.sh"
if [ -f ${dictlo}xml.zip ]
 then
 echo "remove old ${dictlo}xml.zip"
 rm ${dictlo}xml.zip
fi
if [ -f xml ]
 then
  rm -r xml
fi
mkdir xml
echo "copying files from ../pywork to xml/"
cp ../pywork/${dictlo}.dtd xml/
cp ../pywork/${dictlo}.xml xml/
cp ../pywork/${dictlo}-meta2.txt xml/
cp ../pywork/${dictlo}header.xml xml/

echo "create new ${dictlo}xml.zip"
zip -rq ${dictlo}xml.zip xml
# clean up. Remove xml directory
rm -r xml
