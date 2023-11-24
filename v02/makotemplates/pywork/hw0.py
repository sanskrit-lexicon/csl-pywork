# coding=utf-8
# hw0.py 2017-05-19
# input: xxxhw.txt 
# output: xxxhw0.txt
import re
import sys,codecs
from hwparse import init_hwrecs

def write(hw0recs,fileout):
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in hw0recs:  # rec is a string
   f.write(rec + '\n')

def extract_hw0_helper(rec):
 # rec is HW objet
 # all records get pc:k1:ln1,ln2:L
 ln1 = rec.ln1
 ln2 = rec.ln2
 pc = rec.pc
 k2 = rec.k2
 L = rec.L
 out1 = '%s:%s:%s,%s:%s' %(pc,k2,ln1,ln2,L)
 if rec.type == None:
  out2 = ''
 else:
  # For alternate headwords, one more field  type,LP
  out2 = ':%s,%s' %(rec.type,rec.LP)
 out = out1 + out2
 return out

def extract_hw0(hwrecs):
 recs2 = []  # an array of strings
 for rec in hwrecs:
  # rec is HW object
  # construct HW0 object by excluding key2
  # out1 = '%s:%s:%s:%s,%s:%s' %(pc,key1,key2,linenum1,linenum2,L)
  rec2 = extract_hw0_helper(rec)
  recs2.append(rec2)
 return recs2

if __name__ == "__main__":
 filein = sys.argv[1]   # xxxhw.txt
 fileout = sys.argv[2]
 hwrecs = init_hwrecs(filein)
 hw0recs = extract_hw0(hwrecs)
 write(hw0recs,fileout)
