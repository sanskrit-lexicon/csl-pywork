# generate (update or initialize) orig, pywork, and web 
# code for a given dictionary  (uses csl-websanlexicon/v02)
#  usage: sh generate_dict.sh <dict> <parent-dir>
#  The files are put into <parent-dir>.
if [ -z "$1" ] || [ -z "$2" ]
  then
   echo "usage:  sh generate_dict.sh <dict> <parent-dir>"
   echo "Example: sh generate_dict.sh acc tempparent/acc"
   echo "Example: sh generate_dict.sh acc ../../ACCScan/2020"
   exit 1
  else
     dict=$1  # assume lower-case
     outdir=$2
fi

DICT_UPPER=$(echo "$dict" | tr '[:lower:]' '[:upper:]')
printf "\033[34mGENERATING %s DICTIONARY DISPLAY AT %s\033[0m\n" "$DICT_UPPER" "$outdir"

curdir=`pwd`  # so we can get back here
# generate_orig.sh must be executed with 'bash'
echo "BEGIN generate_orig.sh $dict $outdir"
output=$(bash generate_orig.sh "$dict" "$outdir" 2>&1)
if [ -n "$output" ]; then
  printf "\033[31m%s\033[0m\n" "$output"
fi
echo "END generate_orig.sh $dict $outdir"

echo "BEGIN generate_pywork.sh $dict $outdir"
output=$(sh generate_pywork.sh "$dict" "$outdir" 2>&1)
if [ -n "$output" ]; then
  printf "\033[31m%s\033[0m\n" "$output"
fi
echo "END generate_pywork.sh $dict $outdir"

# resolve $outdir to full path 
fullpath=`readlink -f $outdir`

cd ../../csl-websanlexicon/v02

echo "BEGIN generate_web.sh $dict $outdir"
output=$(sh generate_web.sh "$dict" "$fullpath" 2>&1)
if [ -n "$output" ]; then
  printf "\033[31m%s\033[0m\n" "$output"
fi
echo "END generate_web.sh $dict $outdir"

cd $curdir # back here
# ---------------------------------------------------------
# Recompute derived files
echo ""
echo "BEGIN execution of pywork code at $outdir/pywork"
cd $outdir/pywork
echo "regenerate $dict headwords"
output=$(sh redo_hw.sh 2>&1)
printf "%s\n" "$output" | awk '
/BEGIN hw\.py$/ { in_hw=1; hw_sub=0; sub_depth=0; print; next }
/BEGIN hw\.py / { if (in_hw) { hw_sub=1 } else { in_hw=1; hw_sub=0; print } next }
/BEGIN init_entries_kosha$/ { hw_sub=1; next }
/BEGIN hw2\.py$/ { in_hw2=1; block=$0; hw2_lines=0; next }
/BEGIN hw0\.py$/ { in_hw0=1; block=$0; hw0_lines=0; next }
/BEGIN / { if (hw_sub) { sub_depth++ } next }
/END hw\.py$/ {
  in_hw=0; hw_sub=0; sub_depth=0; print; next
}
/END hw\.py / { if (hw_sub) hw_sub=0; next }
/END write_entries$/ { hw_sub=0; next }
/END hw2\.py$/ {
  in_hw2=0
  if (hw2_lines > 0) { printf "\033[31m%s\n%s\033[0m\n", block, $0 }
  else { print block; print }
  next
}
/END hw0\.py$/ {
  in_hw0=0
  if (hw0_lines > 0) { printf "\033[31m%s\n%s\033[0m\n", block, $0 }
  else { print block; print }
  next
}
/END / { if (hw_sub && sub_depth > 0) sub_depth--; next }
in_hw {
  ok=0
  if ($0 ~ /^[0-9]+ extra headwords from hwextra\/.*_hwextra\.txt$/) ok=1
  if ($0 ~ /^[0-9]+ lines read from \.\.\/orig\/.*\.txt$/) ok=1
  if ($0 ~ /^[0-9]+ entries found$/) ok=1
  if ($0 ~ /^[0-9]+ lines written to .*hw\.txt$/) ok=1
  if ($0 ~ /^BEGIN /) ok=1
  if ($0 ~ /^END /) ok=1
  if (ok) { print }
  else { printf "\033[31m%s\033[0m\n", $0 }
  next
}
in_hw2 { hw2_lines++; block = block "\n" $0; next }
in_hw0 { hw0_lines++; block = block "\n" $0; next }
{ print }
'

echo "regenerate $dict.xml and postxml files"
output=$(sh redo_xml.sh 2>&1)
printf "%s\n" "$output" | awk '
/BEGIN make_xml\.py$/ { in_xml=1; xml_line=0; print; next }
/END make_xml\.py$/ { in_xml=0; print; next }
/BEGIN xmllint_err$/ { in_xlint=1; next }
/END xmllint_err$/ { in_xlint=0; next }
in_xlint { printf "\033[31m%s\033[0m\n", $0; next }
in_xml {
  xml_line++
  ok=0
  if ($0 == "make_xml.py BEGINS !!!!!") ok=1
  if ($0 == "All records parsed by ET") ok=1
  if ($0 == "make_xml.py ENDS !!!!!") ok=1
  if (ok) { print }
  next
}
{ print }
'

sh redo_postxml.sh
cd $curdir  # back to v02
# Recompute downloads directory
echo "regenerate downloads "
cd $outdir/downloads
sh redo_all.sh
cd $curdir # back to v02
echo "*****************************************************"

