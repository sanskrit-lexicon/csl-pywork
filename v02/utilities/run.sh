#!/bin/bash

for i in $(ls ../../../ | egrep -v csl-) ; do for f in $(find ../../../$i/pywork -name '*.xml' | egrep -v header); do ./parse.py $f ../makotemplates/pywork/one.dtd ;done; done > res 2> err
