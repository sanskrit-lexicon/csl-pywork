# coding=utf-8
"""bibrec.py
   07-19-2018.  This is for pw. The ascode field
   differs from that of pwg, in that it is absent in pwbib.txt
"""
from __future__ import print_function
import re,codecs,sys

class Bibrec(object):
 # Revised 12-11-2017 to recognize 'iast' attribute on <HI>
 d = {}  # dictionary with key = code
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  m = re.search(r'^(.*?) (.*)$',line)
  try:
   lineid = m.group(1)
   body = m.group(2)
  except:
   print("abbrv4 Bibrec init error: line=\n",line.encode('utf-8'))
   exit(1)
  self.lineid=lineid
  # entryflag indicates to caller that this record is/is-not an entry record
  self.entryflag=False 
  #if lineid == '1.000':
  # return
  #m = re.search(r'^<HI code="(.*?)" *iast="(.*?)".*?>(.*)$',body)
  m = re.search(r'^<HI iast="(.*?)".*?>(.*)$',body)
  if not m:
   # [Page...],
   # [Volume...]
   print("SKIPPING LINE",body.encode('utf-8'))
   return 
  #if m.group(1) == '':
  # return  # incomplete records.
  self.ascode = None   # AS encoding (letter-number)
  self.code = m.group(1)
  self.text = m.group(2)
  """
  if self.code.startswith('*'):  
   # This is not a feature in pwbib.txt.
   # leading asterisk has some meaning in Bibliography
   # but is not needed for matching
   print("Bibrec: removing asterisk from",self.code.encode('utf-8'))
   self.code = self.code[1:] 
  # some codes are of form A oder B. Replace these with A
  #m = re.search(r'^(.*?) oder (.*?)$',self.ascode)
  #if m:
  # self.ascode = m.group(1)
  ## update dictionary
  """
  if self.code in Bibrec.d:
   print("Bibrec skip duplicate iast:",self.code.encode('utf-8'),self.lineid)
   print("Previous lineid with this code is",Bibrec.d[self.code].lineid)
   return
  Bibrec.d[self.code] = self
  self.used = False  # do any references match to this one?
  self.entryflag=True

def init_bibrecs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs=[]
  for x in f:
   if x.startswith(';'):
    continue # comment
   rec = Bibrec(x )
   if rec.entryflag:
    recs.append(rec)
 return recs

def prepare_bibrec_codes(bibrecs):
 codes = [r.code for r in bibrecs if hasattr(r,'code')]
 #print(len(codes),"codes in bibrecs")
 d = {}
 for code in codes:
  a = code[0] # first letter
  if a not in d:
   d[a] = []
  d[a].append(code)
 # sort d[a] by decreasing length
 for a in d:
  d[a] = sorted(d[a],key = lambda x: len(x),reverse=True)
 return d

def match_best_prefix(txt,dcodes):
 """ Assume dcodes is a dictionary with keys which are letters.
  For each letter x, assume dcodes[x] is a list  of strings.
  Do a search of dcodes[x] where x is the first letter of 'txt'.
  Return the first member Y of dcodes[x] which STARTS txt  (i.e., is a
  prefix of txt).  Normally expected to be used when dcodes[x] is
  sorted by decreasing length, so we get the longest match. Return that
  Y.
  Return None if any failure.
 """
 a0 = txt[0]  # the first character of text
 if a0 not in dcodes:
  # no match
  return None
 codes = dcodes[a0] # codes whose first letter is same as that of 'a'
 for code in codes:
  # revised 12-03/2017 to check FULL match ???
  if txt.startswith(code):
   return code
 return None

if __name__ == "__main__":
 filebib = sys.argv[1]
 filetest = sys.argv[2]
 
 bibrecs = init_bibrecs(filebib)
 print(len(bibrecs),"records from",filebib)
 dcodes = prepare_bibrec_codes(bibrecs)
 with codecs.open(filetest,"r","utf-8") as f:
  txts = [x.rstrip('\r\n') for x in f]
 for txt in txts:
  ans = match_best_prefix(txt,dcodes)
  out = "%s  -> %s" %(txt,ans)
  print(out.encode('utf-8'))
