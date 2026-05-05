# coding=utf-8
"""check_pwbib.py  (pwg)
   Validates pwgbib_input.txt before it is loaded into pwgbib.sqlite.
   Checks that every line has exactly 4 tab-separated fields and that
   the id field (column 0) is unique across the file.

   Usage: python3 check_pwbib.py <filein>
     <filein>  tab-separated bibliography input file (e.g. pwgbib_input.txt)
   Exits cleanly with a summary; prints WARNINGs for any violations.
"""
from __future__ import print_function
import sys
if __name__ == "__main__":
 filebib = sys.argv[1]
 n = 0
 d = {}
 with open(filebib, 'r', encoding='utf-8') as f:
  for i,line in enumerate(f):
   line = line.rstrip('\r\n')
   lnum = i+1
   parts = line.split('\t')
   if len(parts) != 4:
    print('WARNING: line %s does not have 4 fields' %lnum)
    print(line)
    n = n + 1
   ident = parts[0]
   if ident in d:
    print('WARNING: id "%s" at line %s duplicate of id at line %s' %(ident,lnum,d[ident]))
    n = n + 1
   d[ident] = lnum
 #
 if n != 0:
  print('WARNING:',n,"problems with",filebib)
 else:
  print(filebib,"passes inspection by check_pwbib")
  
