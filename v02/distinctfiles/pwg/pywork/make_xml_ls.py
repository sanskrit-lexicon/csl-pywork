# coding=utf-8
""" make_xml_ls.py for pwg. 
 Mar 3, 2017.  
 Revised 12-14-2017
 Reads 
  previous version of pwg.xml and
  
 Adds 'n="..."' attribute to selected <ls> elements
"""
from __future__ import print_function
import sys, re, codecs
sys.path.append('pwgauth')
from bibrec import Bibrec,init_bibrecs,prepare_bibrec_codes,match_best_prefix

def adjust_ls_old(line,lsdict):
 #global ncalls
 def adjust_ls_helper(m):
  """ define with adjust_ls so that lsdict is available 
  """
  abbrvtxt = m.group(1)
  if abbrvtxt in lsdict:
   lsrec = lsdict[abbrvtxt]
   attr = 'n="%s"' % lsrec.bibid
   return "<ls %s>%s</ls>" %(attr,abbrvtxt)
  else:
   # no change
   return m.group(0)
 # now apply the substitution
 line1 = re.sub(r'<ls>(.*?)</ls>',adjust_ls_helper,line)
 return line1

def adjust_ls(line,dcodes):
 lsarr = re.findall(r'<ls>.*?</ls>',line)
 changes = []
 # get array of changes, if any
 for ls in lsarr:
  m = re.search(r'<ls>(.*?)</ls>',ls)
  abbrv = m.group(1)
  code = match_best_prefix(abbrv,dcodes)
  if code == None:
   continue
  rec = Bibrec.d[code]  # the underlying Bibrec object
  n = rec.lineid
  new = '<ls n="%s">%s</ls>' %(n,abbrv)
  changes.append((ls,new))
 # apply the changes
 line1 = line
 for old,new in changes:
  line1 = line1.replace(old,new)
 return line1
def make_xmlfun(filein,dcodes,fileout):
 # slurp txt file into list of lines
 nadj = 0
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  with codecs.open(fileout,encoding='utf-8',mode='w') as fout:
   for line in f:
    line1 = adjust_ls(line,dcodes)
    if line1 != line:
     nadj = nadj + 1
     if nadj > 5000000:
      print("DEBUG Quitting after",nadj,"changes")
      break
    fout.write(line1)

 print(nadj,"lines changed")

if __name__=="__main__":
 filein = sys.argv[1] # pwg0.xml
 filebib = sys.argv[2] #pwgbib
 fileout = sys.argv[3] # pwg.xml
 #lsdict = init_lsdata(filein1)
 bibrecs = init_bibrecs(filebib)
 dcodes = prepare_bibrec_codes(bibrecs)

 make_xmlfun(filein,dcodes,fileout)
