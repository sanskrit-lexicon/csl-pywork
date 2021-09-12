dict=$1
xml=../../$dict/pywork/$dict.xml
dtd=../../$dict/pywork/$dict.dtd
cmd="python3 ../../xmlvalidate.py $xml $dtd"
echo $cmd
$cmd

