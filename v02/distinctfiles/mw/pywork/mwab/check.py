# coding=utf-8
"""check.py for mwab
   check uniqueness of abbreviation.
   This required for Cologne sqlite construction.
"""
from __future__ import print_function
import re,codecs,sys
if __name__ == "__main__":
 numfields = int(sys.argv[1])
 filein = sys.argv[2]
 n = 0
 d = {}
 with codecs.open(filein,"r","utf-8") as f:
  for i,line in enumerate(f):
   line = line.rstrip('\r\n')
   lnum = i+1
   parts = line.split('\t')
   nparts = len(parts)
   if nparts != numfields:
    print('WARNING: line %s does not have %s fields' % (lnum,nparts))
    print(line)
    n = n + 1
   ident = parts[0]
   if ident in d:
    print('WARNING: id "%s" at line %s duplicate of id at line %s' %(ident,lnum,d[ident]))
    n = n + 1
   d[ident] = lnum
 #
 if n != 0:
  print('WARNING:',n,"duplicate problems with",filein)
 else:
  print(filein,"passes inspection by check.py")
  
