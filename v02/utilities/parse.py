#!/usr/bin/python
from lxml import objectify
import re,sys,pprint
pp = pprint.PrettyPrinter(indent=4)

filexml = sys.argv[1]
filedtd = sys.argv[2]

attrs={}; c={}
with open(filedtd,"r") as f:
 for ln in f:
  if ln.startswith("<!ATTLIST"): 
   r=ln.split(); elt=r[1]; attr=r[2]
   if elt not in attrs: attrs[elt]={}
   if attr not in attrs[elt]: attrs[elt][attr]={}
   if "CDATA" not in ln: 
    for i in re.findall(r'\((.*?)\)',ln)[0].split('|'):
     attrs[elt][attr][i.lstrip().rstrip()]=1

def iter(i):
 if i.tag: 
  if i.tag not in c: 
   c[i.tag] = {}; c[i.tag]['_cnt_']=0
  c[i.tag]['_cnt_']=c[i.tag]['_cnt_']+1
  for a in i.attrib.keys():
   if len(attrs[i.tag][a])>0:
    if a not in c[i.tag]: c[i.tag][a]={}
    if i.attrib[a] not in c[i.tag][a]: c[i.tag][a][i.attrib[a]]=0
    c[i.tag][a][i.attrib[a]]=c[i.tag][a][i.attrib[a]]+1
   else:
    if a not in c[i.tag]: c[i.tag][a]=0
    c[i.tag][a]=c[i.tag][a]+1
 for m in i.getchildren(): iter(m)

iter(objectify.parse(filexml).getroot())
print "--- %s ---"%(filexml)
pp.pprint(c)
 

