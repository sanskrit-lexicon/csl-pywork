#!/bin/bash
# generate_dict.sh
# Main entry point for generating or updating a complete dictionary installation.
#
# Usage: sh generate_dict.sh <dict> <outdir>
#   <dict>    lowercase dictionary code (e.g. mw, skd, acc)
#   <outdir>  target directory (created if it does not exist)
#             e.g. ../../MWScan/2020  or  tempparent/mw
#
# Runs four stages in sequence:
#   1. generate_orig.sh    — copies source text from csl-orig into outdir/orig/
#   2. generate_pywork.sh  — assembles outdir/pywork/ from makotemplates/ and distinctfiles/
#   3. generate_ab_bib_ls.sh — generates abbreviation/tooltip/bibliography redo scripts
#   4. generate_web.sh     — assembles outdir/web/ (runs from csl-websanlexicon/v02)
# Then executes the assembled scripts:
#   redo_hw.sh    — builds xxxhw.txt headword file
#   redo_xml.sh   — builds xxx.xml, validates against xxx.dtd, runs redo_postxml.sh
#   downloads/redo_all.sh — builds zip download archives
#
# Prerequisites: csl-websanlexicon must be a sibling of csl-pywork.
# generate (update or initialize) orig, pywork, and web
# code for a given dictionary  (uses csl-websanlexicon/v02)
unset CDPATH
if [ -z "$1" ] || [ -z "$2" ]
  then
   echo "usage:  sh generate_dict.sh <dict> <parent-dir>"
   echo "Example: sh generate_dict.sh acc tempparent/acc"
   echo "Example: sh generate_dict.sh acc ../../ACCScan/2020"
   exit 1
  else
     dict=$1  # assume lower-case
     outdir="${2%/}"
fi

DICT_UPPER=$(echo "$dict" | tr '[:lower:]' '[:upper:]')
printf "\033[34mGENERATING %s DICTIONARY DISPLAY AT %s\033[0m\n" "$DICT_UPPER" "$outdir"

curdir=`pwd`  # so we can get back here
# P5: fail-closed helper — print a red STOP marker (visible to red-line
# gates such as csl-orig scripts/check_generate_dict.sh) and exit nonzero
# so callers never build on a half-assembled tree.
fail_exit() {
  cd "$curdir" 2>/dev/null
  printf "\033[31mSTOP generate_dict.sh: %s\033[0m\n" "$1"
  exit 1
}
# generate_orig.sh must be executed with 'bash'
echo "BEGIN generate_orig.sh $dict $outdir"
output=$(bash generate_orig.sh "$dict" "$outdir" 2>&1)
stage_status=$?
if [ -n "$output" ]; then
  printf "\033[31m%s\033[0m\n" "$output"
fi
echo "END generate_orig.sh $dict $outdir"
if [ $stage_status -ne 0 ]; then fail_exit "generate_orig.sh exited with status $stage_status"; fi

echo "BEGIN generate_pywork.sh $dict $outdir"
output=$(sh generate_pywork.sh "$dict" "$outdir" 2>&1)
stage_status=$?
if [ -n "$output" ]; then
  printf "\033[31m%s\033[0m\n" "$output"
fi
echo "END generate_pywork.sh $dict $outdir"
if [ $stage_status -ne 0 ]; then fail_exit "generate_pywork.sh exited with status $stage_status"; fi

# Generate ab/bib/ls sqlite scripts directly into target pywork directory
echo "BEGIN generate_ab_bib_ls.sh $dict $outdir"
sh generate_ab_bib_ls.sh "$dict" "$outdir/pywork"
stage_status=$?
echo "END generate_ab_bib_ls.sh $dict $outdir"
if [ $stage_status -ne 0 ]; then fail_exit "generate_ab_bib_ls.sh exited with status $stage_status"; fi

# resolve $outdir to full path
fullpath=`readlink -f $outdir`
if [ ! -d "$fullpath" ]; then fail_exit "readlink -f $outdir failed"; fi

cd ../../csl-websanlexicon/v02 || fail_exit "cd ../../csl-websanlexicon/v02 failed"

echo "BEGIN generate_web.sh $dict $outdir"
output=$(sh generate_web.sh "$dict" "$fullpath" 2>&1)
stage_status=$?
if [ -n "$output" ]; then
  printf "\033[31m%s\033[0m\n" "$output"
fi
echo "END generate_web.sh $dict $outdir"
if [ $stage_status -ne 0 ]; then fail_exit "generate_web.sh exited with status $stage_status"; fi

cd $curdir || fail_exit "cd back to $curdir failed"
# ---------------------------------------------------------
# Recompute derived files
echo ""
echo "BEGIN execution of pywork code at $outdir/pywork"
cd $outdir/pywork || fail_exit "cd $outdir/pywork failed"
echo "regenerate $dict headwords"
output=$(sh redo_hw.sh 2>&1)
redo_hw_status=$?
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

if [ $redo_hw_status -ne 0 ]; then fail_exit "redo_hw.sh exited with status $redo_hw_status"; fi

echo "regenerate $dict.xml and postxml files"
output=$(sh redo_xml.sh 2>&1)
redo_xml_status=$?
printf "%s\n" "$output" | awk -v dict="$dict" '
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
  if (dict == "vcp" && $0 ~ /^Unexpected <H>:/) ok=1
  if (ok) { print }
  else { printf "\033[31m%s\033[0m\n", $0 }
  next
}
{ print }
'

if [ $redo_xml_status -ne 0 ]; then fail_exit "redo_xml.sh exited with status $redo_xml_status"; fi

sh redo_postxml.sh
stage_status=$?
if [ $stage_status -ne 0 ]; then fail_exit "redo_postxml.sh exited with status $stage_status"; fi
cd $curdir  # back to v02
# Recompute downloads directory
echo "regenerate downloads "
cd $outdir/downloads || fail_exit "cd $outdir/downloads failed"
sh redo_all.sh
stage_status=$?
if [ $stage_status -ne 0 ]; then fail_exit "downloads/redo_all.sh exited with status $stage_status"; fi
cd $curdir || fail_exit "cd back to $curdir failed" # back to v02
echo "*****************************************************"

