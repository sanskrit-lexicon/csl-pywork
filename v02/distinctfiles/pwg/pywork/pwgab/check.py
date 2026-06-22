""" check.py
Check validity of pwgab_input.txt
"""
from __future__ import print_function

import sys,re

if __name__ == '__main__':

 filein = sys.argv[1]

 with open(filein, encoding='utf-8') as f:
  lines = [line.rstrip('\r\n') for line in f]
 print(len(lines), 'lines read from', filein)
 num_cols = 2
 regex = '<id>(.*?)</id>.*?<disp>(.*?)</disp>'
 d = {}
 nprob = 0
 for iline,line in enumerate(lines):
  parts = line.split('\t')
  if len(parts) != num_cols:
   print('WARNING: expected %d columns, got %d in line: %s' % (num_cols, len(parts), line))
   continue
  abbrev = parts[0]
  data = parts[1]
  if abbrev in d:
   print(f'Duplicate abbrev {abbrev} at line {iline+1}')
   nprob = nprob + 1
   continue
  else:
   d[abbrev] = data
  m = re.search(regex,data)
  if m == None:
   nprob = nprob + 1
   print(f'ERROR in data at line {iline+1}')
   print(f'  using regex {regex}')
   continue
  ab = m.group(1)
  if ab != abbrev:
   nprob = nprob + 1
   print(f'<id>{ab}</id> inconsistent with {abbrev} at line {iline+1}')
 print(f'# of problems = {nprob}')
 
  
