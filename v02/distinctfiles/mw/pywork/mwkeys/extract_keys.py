"""extract_keys.py April 8, 2015
 Conversion of extract_keys.php to Python
 Read a version of monier.xml, and construct extract_keys.txt.
 04-04-2018. Revised to use hwkeys.txt as input
 
"""
from __future__ import print_function
import sys, re,codecs
sys.path.append('../')  # pywork
import hwparse
def old_extract_keys(filein,fileout):
 fout = codecs.open(fileout,"w",'utf-8')
 f = codecs.open(filein,"r",'utf-8')
 n = 0 # number of lines read
 nout = 0 # Number of lines written
 for line in f:
  n = n + 1
  m = re.search(r'<(H[^>]*)>.*?<key1>(.*?)</key1>.*?<L.*?>(.*?)</L>',line)
  if not m: # skip boilerplate
   continue
  # line = line.rstrip('\r\n')
  cat = m.group(1)
  key = m.group(2)
  L = m.group(3)
  fout.write('%s,%s,%s\n' %(key,cat,L))
  nout = nout + 1
 f.close()
 fout.close()
 print(n,"records in,",nout,"records written")

def extract_keys(filein,fileout):
 fout = codecs.open(fileout,"w",'utf-8')
 hwrecs = hwparse.init_hwrecs(filein)
 #f = codecs.open(filein,"r",'utf-8')
 n = 0 # number of lines read
 nout = 0 # Number of lines written
 for r in hwrecs:
  n = n + 1
  #m = re.search(r'<(H[^>]*)>.*?<key1>(.*?)</key1>.*?<L.*?>(.*?)</L>',line)
  #if not m: # skip boilerplate
  # continue
  # line = line.rstrip('\r\n')
  cat = 'H' + r.e
  key = r.k1
  L = r.L
  #key = m.group(2)
  #L = m.group(3)
  fout.write('%s,%s,%s\n' %(key,cat,L))
  nout = nout + 1
 #f.close()
 fout.close()
 print(n,"records in,",nout,"records written")

if __name__=="__main__": 
 filein = sys.argv[1] #  monier.xml
 fileout = sys.argv[2] # extract_keys.txt
 extract_keys(filein,fileout)
