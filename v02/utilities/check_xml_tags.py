""" check_xml_tags.py (generic)
"""
from __future__ import print_function
import re,sys
import codecs

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
 with codecs.open(fileout,'w','utf-8') as f:
  for out in outarr:
   f.write(out + '\n')
 print(len(keys),"lines written to",fileout)

#-----------------------------------------------------
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 d = tagfreqs(lines)
 write_tags(d,fileout)
