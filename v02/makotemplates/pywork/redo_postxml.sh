# 
# 0. copy xxxheader.xml from pywork to web
echo "BEGIN pywork/redo_postxml.sh"
pwd
echo "cp ${dictlo}header.xml ../web/"
cp ${dictlo}header.xml ../web/
echo ""
# 1. Redo web/xxx.sqlite
echo "BEGIN sqlite"
cd sqlite
output=$(sh redo.sh 2>&1)
printf "%s\n" "$output" | awk '
{
  ok=0
  if ($0 ~ /^remaking .*\.sqlite from \.\..*\.xml with python\.\.\.$/) ok=1
  if ($0 ~ /^sqlite\.py: dictionary code= .*$/) ok=1
  if ($0 ~ /^[0-9]+ lines read from \.\.\/.*\.xml$/) ok=1
  if ($0 ~ /^create_index takes [0-9.]+ seconds$/) ok=1
  if ($0 ~ /^[0-9]+ rows written to .*\.sqlite$/) ok=1
  if ($0 ~ /^[0-9.]+ seconds for batch size [0-9]+$/) ok=1
  if ($0 ~ /^moving .*\.sqlite to web\/sqlite\/$/) ok=1
  if (ok) { print }
  else { printf "\033[31m%s\033[0m\n", $0 }
}
'
cd ../ # back in pywork
echo "END sqlite"
# 2. redo db (query_dump) for advanced search
cd webtc2
sh redo.sh
cd ../ # back to pywork
# For applicable dictionaries, update other web/sqlite databases
# abbreviations
%if dictlo in ['ben','stc','bur','cae','mw','pw','pwg','lan','gra','ap90','pwkvn','bhs','md','ap']:
 cd ${dictlo}ab
 sh redo.sh
 cd ../ # back to pywork
%endif
# literary source.
%if dictlo in ['mw','pw','pwg','ap90','ben','pwkvn','sch','gra','bhs','ap']:
 cd ${dictlo}auth
 sh redo.sh
 cd ../ # back to pywork
%endif
# two extra links dbs for mw
%if dictlo == 'mw':
 # Westergaard DAtupAWa links
 cd westmwtab
 sh redo.sh
 cd ../ # back to pywork
 # Whitney roots links.
 cd whitmwtab
 sh redo.sh
 cd ../ # back to pywork
%endif
