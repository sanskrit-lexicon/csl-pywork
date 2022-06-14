# coding=utf-8
"""bibrec.py
   07-19-2018.  This is for pw. The ascode field
   differs from that of pwg, in that it is absent in pwbib.txt
"""
from __future__ import print_function
import re,codecs,sys
if __name__ == "__main__":
 filebib = sys.argv[1]
 n = 0
 d = {}
 with codecs.open(filebib,"r","utf-8") as f:
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
  
