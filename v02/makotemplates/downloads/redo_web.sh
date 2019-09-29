echo "BEGIN: downloads/redo_web1.sh"
if [ -f ${dictlo}web1.zip ]
 then
 echo "remove old ${dictlo}web1.zip"
 rm ${dictlo}web1.zip
fi
cd ../
zip  -rq downloads/${dictlo}web1.zip web -x *pdfpages*
cd downloads
