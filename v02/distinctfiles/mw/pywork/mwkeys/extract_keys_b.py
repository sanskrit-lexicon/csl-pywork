"""extract_keys_b.py April 8, 2015
 Conversion of extract_keys_b.php to Python
 Read extract_keys.txt, and construct extract_keys_b.txt.
 
"""
from __future__ import print_function
import sys, re,codecs
import string
pyversion2 = (sys.version_info[0] == 2)

# Note 'L' and '|' and 'Z' and 'V' are not present
# Not sure where they go 
tranfrom="aAiIuUfFxXeEoOMHkKgGNcCjJYwWqLQ|RtTdDnpPbBmyrlvSzsh"
tranto = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxy"
# ref: https://stackoverflow.com/questions/41708770/translate-function-in-python-3
if pyversion2:
 trantable = string.maketrans(tranfrom,tranto)
else: #version3 of python
 trantable = str.maketrans(tranfrom,tranto)

def translate_one(a):
 if pyversion2:
  a1 = string.translate(a,trantable)
 else:
  a1 = a.translate(trantable)
 return a1

def slp_cmp(a,b):
 try:
  #a1 = string.translate(a,trantable)
  #b1 = string.translate(b,trantable)
  a1 = translate_one(a)
  b1 = translate_one(b)
 except:
  print("slp_cmp error: a=",a,"b=",b)
  exit(1)
 return cmp(a1,b1)

def extract_keys_b(filein,fileout):
 fout = codecs.open(fileout,"w",'utf-8')
 f = codecs.open(filein,"r",'utf-8')
 n = 0 # number of lines read
 # state variables
 keyhash = {}
 for line in f:
  n = n + 1
  if n > 1000000: #50:
   print("Debug breaking")
   break
  line = line.rstrip('\r\n')
  (key,hcode,L1,L2) = re.split(',',line)
  out1 = "%s,%s,%s" %(hcode,L1,L2)
  if key in keyhash:
   keyhash[key] = "%s;%s" %(keyhash[key],out1)
  else:
   keyhash[key] = out1
 # done with loop
 f.close()
 # for slp_cmp to work (namely, string.translate, need array of ascii keys
 keys = []
 for key in keyhash:  
  if pyversion2:
   key = key.decode("utf-8").encode("ascii","ignore")
  keys.append(key)
 # sort keys  into Sanskrit alphabetical order
 if pyversion2:
  sorted_keys = sorted(keys,cmp=slp_cmp)
 else:
  sorted_keys = sorted(keys,key=lambda x: translate_one(x))
 #--- output phase
 nout = 0
 for key1 in sorted_keys:
  out = keyhash[key1]
  nout = nout+1
  fout.write("%s\t%s\t%s\n" % (key1,nout,out))
 fout.close()
 # summary messages
 print(n,"records in",filein)
 print(nout,"records written to",fileout)

if __name__=="__main__": 
 filein = sys.argv[1] #  extract_keys_a.txt
 fileout = sys.argv[2] # extract_keys_b.txt
 extract_keys_b(filein,fileout)
