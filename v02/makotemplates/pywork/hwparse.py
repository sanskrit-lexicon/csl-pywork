"""hwparse.py
   08-14-2017
   HW class
   init_hwrecs(filein)  function to read xxxhw.txt and return
    array of HW records.
"""
from __future__ import print_function
import re,codecs
from parseheadline import parseheadline
class HW(object):
 Ldict = {}  # dictionary into all HW records, key = L
 Sanskrit = True  # the headwords of this dictionary are Sanskrit.
 dictcode = '${dictlo}' 
 # all keys that COULD occur  
 # hom -> h, 09-16-2017
 if dictcode == 'mw':
  hwrec_keys = ['L','pc','k1','k2','h'] +\
               ['type','LP','k1P'] +\
               ['ln1','ln2','e']
 else:
  hwrec_keys = ['L','pc','k1','k2','h'] +\
               ['type','LP','k1P'] +\
               ['ln1','ln2']
  

 def __init__(self,line):
  """
    If 'rec' is an instance of this object, then we may refer to
    the 'L' (and others in hwrec_keys) attributes in one of two ways:
    rec.d['L'] or
    rec.L
  """
  line = line.strip() # remove starting or ending whitespace
  self.line = line
  d = parseheadline(line)
  for k in self.hwrec_keys:
   if k not in d:
    d[k] = None  # default value
  self.d = d
  # also, unpack d into object attributes
  # for simplicity, use the attribute names as key names.
  for k in d:
   setattr(self,k,d[k])
%if dictlo not in ['abch']:
  # update Ldict
  if self.L in self.Ldict:
   print("HW_init ERROR: duplicate L-code=",self.L)
   exit(1)
  self.Ldict[self.L]=self
%endif

def init_hwrecs(filein):
 recs=[]
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  n = 0
  for line in f:
   n = n + 1
   rec = HW(line)
   recs.append(rec)
 return recs
