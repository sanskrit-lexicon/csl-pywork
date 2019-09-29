echo "BEGIN: downloads/redo_txt.sh"
if [ -f ${dictlo}txt.zip ]
 then
 echo "remove old ${dictlo}txt.zip"
 rm ${dictlo}txt.zip
fi
if [ -f txt ]
 then
  rm -r txt
fi
mkdir txt
echo "copying files from ../pywork to txt/"
cp ../orig/${dictlo}.txt txt/
cp ../pywork/${dictlo}-meta2.txt txt/
cp ../pywork/${dictlo}header.xml txt/

echo "create new ${dictlo}txt.zip"
zip -rq ${dictlo}txt.zip txt
# clean up. Remove txt directory
rm -r txt
