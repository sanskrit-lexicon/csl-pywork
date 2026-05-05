"""check_xml_tags.py
   Counts the frequency of every XML tag in a file and writes a sorted report.

   Usage: python3 check_xml_tags.py <filein> <fileout>
     <filein>   any text file containing XML-style tags
     <fileout>  output file: one line per distinct tag, format: COUNT TAG
                sorted alphabetically by tag name (ignoring the leading slash)

   Useful for auditing which tags appear in a digitisation or XML file and
   how often, as a first step when debugging DTD validation failures.
"""
from __future__ import print_function
import re
import sys

def tagfreqs(lines):
 c = {} # counter
 for line in lines:
  tags = re.findall(r'<.*?>',line)
  for tag in tags:
   if tag not in c:
    c[tag] = 0
   c[tag] = c[tag] + 1
 return c
def write_tags(d,fileout):
 keys = d.keys()
 keys = sorted(keys,key=lambda x: x.replace('/',''))
 outarr = []
 for key in keys:
  outarr.append('%06d %s' %(d[key],key))
 with open(fileout, 'w', encoding='utf-8') as f:
  for out in outarr:
   f.write(out + '\n')
 print(len(keys),"lines written to",fileout)

#-----------------------------------------------------
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 with open(filein, 'r', encoding='utf-8') as f:
  lines = [x.rstrip('\r\n') for x in f]
 d = tagfreqs(lines)
 write_tags(d,fileout)
