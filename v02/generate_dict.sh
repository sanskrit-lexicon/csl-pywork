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

curdir=`pwd`  # so we can get back here
# generate_orig.sh must be executed with 'bash'
echo "BEGIN generate_orig.sh $dict $outdir"
bash generate_orig.sh "$dict" "$outdir"
echo "END generate_orig.sh $dict $outdir"
echo ""

echo "BEGIN generate_pywork.sh $dict $outdir"
sh generate_pywork.sh "$dict" "$outdir"
echo "END generate_pywork.sh $dict $outdir"
echo ""

# resolve $outdir to full path 
fullpath=`readlink -f $outdir`

cd ../../csl-websanlexicon/v02

echo "BEGIN generate_web.sh $dict $outdir"
sh generate_web.sh "$dict" "$fullpath"
echo "END generate_web.sh $dict $outdir"
echo ""

cd $curdir # back here
# ---------------------------------------------------------
# Recompute derived files
echo 
echo "*****************************************************"
echo "BEGIN execution of pywork code at $outdir/pywork"
cd $outdir/pywork
echo "regenerate $dict headwords"
sh redo_hw.sh

echo "regenerate $dict.xml and postxml files"
sh redo_xml.sh
cd $curdir  # back to v02
# Recompute downloads directory
echo "regenerate downloads "
cd $outdir/downloads
sh redo_all.sh
cd $curdir # back to v02

