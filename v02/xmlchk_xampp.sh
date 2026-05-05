#!/bin/bash
# xmlchk_xampp.sh
# Validates a generated dictionary XML file against its DTD using xmlvalidate.py.
#
# Usage: sh xmlchk_xampp.sh <dict>
#   <dict>  lowercase dictionary code (e.g. mw, skd)
#
# Assumes XAMPP layout where the generated dictionary directory sits two levels
# above v02/ (e.g. ../../mw/pywork/mw.xml and ../../mw/pywork/mw.dtd).
#
# Delegates to xmlvalidate.py (expected at ../../xmlvalidate.py relative to v02/).
# Exits with a non-zero status if validation fails.

dict=$1
xml=../../$dict/pywork/$dict.xml
dtd=../../$dict/pywork/$dict.dtd
cmd="python3 ../../xmlvalidate.py $xml $dtd"
echo $cmd
$cmd

