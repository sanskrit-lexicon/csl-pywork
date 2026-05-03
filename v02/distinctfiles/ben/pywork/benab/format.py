""" format.py
"""
import sys
import re

class Abbrev(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  abbrev,tooltip = re.split(r' += +',line)
  self.abbrev = abbrev.strip()
  self.tooltip = tooltip.strip()

def init_recs(filein):
 with open(filein, 'r', encoding='utf-8') as f:
  recs = [Abbrev(line) for line in f if not line.startswith(';')]
 print(len(recs),"records read from",filein)
 return recs

def reformat_tip(rec):
 a = rec.abbrev
 b = rec.tooltip
 newtip = '<id>%s</id> <disp>%s</disp>' %(a,b)
 rec.newtip = newtip
 
if __name__ == "__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 recs = init_recs(filein)
 for rec in recs:
  reformat_tip(rec)
 with open(fileout, 'w', encoding='utf-8') as f:
  for rec in recs:
   out = '%s\t%s' %(rec.abbrev,rec.newtip)
   f.write(out + '\n')
 print(len(recs),"records written to",fileout)
 
