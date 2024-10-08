"""hw.py  ejf 2014-06-10
   11-19-2023 kosh
   Major revision 2017-05-18
   inputs:
     orig/xxx.txt
     hwextra/xxx_hwextra.txt
   output: xxxhw.txt
   "hom" -> h
   08-15-2024  Lbody (for alternate/extra headwords)
"""
from __future__ import print_function
import re
import sys,codecs
# next parses key-value pairs coded as <key>val<key1>val1...

from parseheadline import parseheadline

class Hwmeta(object):
 # class variables for efficiency
 # The structure of the 'meta' line
 # Assume meta line within xxx.txt is a sequence of key-value pairs
 # coded as
 # <key>val
%if dictlo == 'mw':
 keysall_list = ['L','pc','k1','k2','h','e']  # standard order
%elif dictlo in ['abch', 'acph', 'acsj']:
 keysall_list = ['L','pc']
%else:
 keysall_list = ['L','pc','k1','k2','h']  # standard order
%endif
 # hom is optional
 keysneeded = set(keysall_list).difference(set(['h']))
 # significance of 'e' unclear. Ignore
 keysall = set(keysall_list)
 def __init__(self,line):
  line = line.rstrip('\r\n')
  d = parseheadline(line)
  # check for validity of keys
  keys = set(d.keys())
  if not(self.keysneeded.issubset(keys)):
   # error
   print("Hwmeta init error",line.encode('utf-8'))
   print("keysneeded=",self.keysneeded)
   print("keys=",keys)
   exit(1)
  self.d = d  
  # convert dictionary to object attributes (except for 'e' = extra)
  self.pc = d['pc']
  self.L = d['L']
%if dictlo not in ['abch', 'acph', 'acsj']:
  self.key1 = d['k1']
  self.key2 = d['k2']
  self.h = None
  if 'h' in d:
   self.h = d['h']
%endif
%if dictlo == 'mw':
  self.e = d['e']
%endif

class Hwextra(object):
 # object read from hwextra/xxx_hwextra.txt is a list of key-value pairs.
 keysall_list = Hwmeta.keysall_list + ['type','LP','k1P']
 # hom is optional. Probably never required.
 # pc will be derived from record for LP
 keysneeded = set(keysall_list).difference(set(['h','pc']))
 def __init__(self,line):
  line = line.rstrip('\r\n')
  d = parseheadline(line)
  # check for validity of keys
  keys = set(d.keys())
  if not(self.keysneeded.issubset(keys)):
   # error
   print("Hwextra init error",line.encode('utf-8'))
   print("keysneeded=",self.keysneeded)
   print("keys=",keys)
   exit(1)
  self.d = d  
  # convert dictionary to object attributes
  self.LP = d['LP']
  self.key1P = d['k1P']
  self.type = d['type']
  self.L = d['L']
  self.key1 = d['k1']
  self.key2 = d['k2']
  self.h = None # default
  if 'h' in d:
   self.h = d['h']
 
def init_hwextra(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  recs = [Hwextra(line) for line in f if not line.startswith(';')]
 return recs

def get_k1(s):
 parts = s.split('-')
 if len(parts) > 2:
  print('WARNING: more than one gender',s)
 return parts[0]

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
  self.metaline = lines[0]
  self.lend = lines[-1]  # the <LEND> line
  self.datalines = lines[1:-1]  # the non-meta lines
  # parse the meta line into an Hwmeta object
  self.meta = Hwmeta(self.metaline)
  self.linenum1 = linenum1
  self.linenum2 = linenum2
%if dictlo in ['abch', 'acph', 'acsj']:
  self.L = self.meta.L
  self.pc = self.meta.pc  
  self.keys = self.init_keys()  # array of headwords
%endif
  L = self.meta.L
  if L in self.Ldict:
   print("Entry init error: duplicate L",L,linenum1)
   exit(1)
  self.Ldict[L] = self
%if dictlo in ['abch', 'acph', 'acsj']:
 def init_keys(self):
  a = []
  d = {}  # used to check duplicates
  for line0 in self.datalines:
   line = re.sub(r'</?s>','',line0)  # 10-22-2023
   m = re.search(r'^<eid>(.*?)<syns>(.*)$',line)
   if m == None:
    continue
   syns_str = m.group(2)
   syn_items = syns_str.split(',')
   syns_k1 = [get_k1(item) for item in syn_items]
   for k1m in syns_k1:
    if k1m not in d:
     a.append(k1m)
     d[k1m] = True
  return a
%else:
 def init_keys(self):
  print('hw.py ERROR init_keys')
  exit(1)
%endif

def init_entries(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 inentry = False  
 idx1 = None
 idx2 = None
 for idx,line in enumerate(lines):
  if inentry:
   if line.startswith('<LEND>'):
    idx2 = idx
    entrylines = lines[idx1:idx2+1]
    linenum1 = idx1 + 1
    linenum2 = idx2 + 1
    entry = Entry(entrylines,linenum1,linenum2)
    recs.append(entry)
    # prepare for next entry
    idx1 = None
    idx2 = None
    inentry = False
   elif line.startswith('<L>'):  # error
    print('init_entries Error 1. Not expecting <L>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <LEND>
    continue
  else:
   # inentry = False. Looking for '<L>'
   if line.startswith('<L>'):
    idx1 = idx
    inentry = True
   elif line.startswith('<LEND>'): # error
    print('init_entries Error 2. Not expecting <LEND>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <L>
    continue
 # when all lines are read, we should have inentry = False
 if inentry:
  print('init_entries Error 3. Last entry not closed')
  print('Open entry starts at line',idx1+1)
  exit(1)

 print(len(lines),"lines read from",filein)
 print(len(recs),"entries found")
 return recs
  
def write_hwrecs(hwrecs,fileout):
 """ hwrecs is a list of dictionaries
   whose keys are a subset of the keys appearing in HWextra records
 """
 with codecs.open(fileout,"w","utf-8") as f:
  nout = 0
%if dictlo == 'mw':
  hwrec_keys = ['L','pc','k1','k2','h','e'] +\
               ['type','LP','k1P'] +\
               ['ln1','ln2']
%else:
  hwrec_keys = ['L','pc','k1','k2','h'] +\
               ['type','LP','k1P'] +\
               ['ln1','ln2']
%endif
  for hwrec in hwrecs:
   # hwrec is a dictionary
   kvparts = []   # sequence of key-value part strings
   for key in hwrec_keys:
    if key not in hwrec:
     continue
    val = hwrec[key]
    if val == None:
     continue
    kvpart = ('<' + '%s>%s') %(key,val)
    kvparts.append(kvpart)
   out = ''.join(kvparts)
   f.write(out + '\n')
   nout = nout+1
 print(nout,"lines written to",fileout)

def entry_to_hwrec(entry):
 """ entry is an Entry object. return a dictionary """
 d = {}
 meta = entry.meta # an Hwmeta object.
 # copy keys of meta.d into d
 for k in meta.d:
  d[k] = meta.d[k]
 # add ln1 and ln2 keys
 d['ln1'] = entry.linenum1
 d['ln2'] = entry.linenum2
 return d

def hwextra_to_hwrec(recx):
 """ recx is an Hwextra object. return a dictionary """
 d = {}
 # copy keys of recx.d into d
 for k in recx.d:
  d[k] = recx.d[k]
 # add ln1 and ln2 keys from the entry with L-number = LP
 # i.e., the xxx.txt lines of Parent are used for this child
 LP = d['LP']
 entryP = Entry.Ldict[LP]
 d['ln1'] = entryP.linenum1
 d['ln2'] = entryP.linenum2
 # also, pc (pagecol) comes from Hwmeta record within entryP
 metaP = entryP.meta
 d['pc'] = metaP.pc
 return d

def entry_to_hwrec_Lbody(entry):
 """ entry is an Entry object. return a dictionary 
  Handle 'extra' (alternate) headwords.
  The body in xxx.txt contains {{Lbody=X}} text.
  Another entry with L=X is used for data lines (ln1,ln2)
 """
 d = {}
 meta = entry.meta # an Hwmeta object.
 # copy keys of meta.d into d
 for k in meta.d:
  d[k] = meta.d[k]
 # add ln1 and ln2 keys
 # default values
 d['ln1'] = entry.linenum1
 d['ln2'] = entry.linenum2
 text = entry.datalines[0] # first data line
 m = re.search('{{Lbody=(.*?)}}',text)
 if m == None:
  return d
 LP = m.group(1)  # parent L id
 if LP not in Entry.Ldict:
  print('hw.py WARNING: Lbody not found:',text)
  return d
 entryP= Entry.Ldict[LP] # parent
 d['ln1'] = entryP.linenum1
 d['ln2'] = entryP.linenum2
 return d

def write_entries_kosha(entries,fileout):
 """ write different format for koshas (abch)
 """
 outarr = []
 for entry in entries:
  L = entry.L
  pc = entry.pc
  ln1 = entry.linenum1
  ln2 = entry.linenum2
  for key in entry.keys:
   k1 = key
   k2 = k1
   out = '<L>%s<pc>%s<k1>%s<k2>%s<ln1>%s<ln2>%s' % (L,pc,k1,k2,ln1,ln2)
   outarr.append(out)
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out + '\n')

def init_entries_kosha(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 inentry = False  
 idx1 = None
 idx2 = None
 for idx,line in enumerate(lines):
  if inentry:
   if line.startswith('<LEND>'):
    idx2 = idx
    entrylines = lines[idx1:idx2+1]
    linenum1 = idx1 + 1
    linenum2 = idx2 + 1
    entry = Entry(entrylines,linenum1,linenum2)
    recs.append(entry)
    # prepare for next entry
    idx1 = None
    idx2 = None
    inentry = False
   elif line.startswith('<L>'):  # error
    print('init_entries Error 1. Not expecting <L>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <LEND>
    continue
  else:
   # inentry = False. Looking for '<L>'
   if line.startswith('<L>'):
    idx1 = idx
    inentry = True
   elif line.startswith('<LEND>'): # error
    print('init_entries Error 2. Not expecting <LEND>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <L>
    continue
 # when all lines are read, we should have inentry = False
 if inentry:
  print('init_entries Error 3. Last entry not closed')
  print('Open entry starts at line',idx1+1)
  exit(1)

 print(len(lines),"lines read from",filein)
 print(len(recs),"entries found")
 return recs

if __name__ == "__main__":
 filedig = sys.argv[1]
 fileextra = sys.argv[2]
 fileout = sys.argv[3]

 recsextra = init_hwextra(fileextra)
 print(len(recsextra),"extra headwords from",fileextra)

% if dictlo in ['abch', 'acph', 'acsj']:
 # abch is kosha. No 'extra headwords
 print ("BEGIN init_entries_kosha")
 entries = init_entries_kosha(filedig)
 write_entries_kosha(entries,fileout)
 print("END write_entries")
% elif dictlo in ['mw','gra','ben','acc','ap90','bur','cae','lrv','pw','pwkvn','shs','skd','vcp','pwg']:
 # 08-27-2024 Lbody. Does not use recsextra
 entries = init_entries(filedig)
 hwrecs = [entry_to_hwrec_Lbody(entry) for entry in entries]
 write_hwrecs(hwrecs,fileout)
% else:
 print("BEGIN hw.py init_entries")
 entries = init_entries(filedig)
 print("END hw.py init_entries")
 # generate list of key-value dictionaries for normal entries
 hwrecs_normal = [entry_to_hwrec(entry) for entry in entries]
 # generate similar list for extra headwords
 hwrecs_extra = [hwextra_to_hwrec(recx) for recx in recsextra]
 # merge the two lists
 hwrecs_all = hwrecs_normal +  hwrecs_extra
 # sort the merged list based on L-code
 hwrecs = sorted(hwrecs_all,key=lambda x: float(x['L']))
 # print the sorted list
 write_hwrecs(hwrecs,fileout)
%endif

