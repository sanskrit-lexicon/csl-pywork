#!/usr/bin/python
from lxml import objectify
import re,sys,codecs
import os.path

attrs={}; c={}; c23={}; c32={}

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
 
def sort_tags(d):
 keys=c.keys()
 keys=sorted(keys)
 if d not in c23.keys(): c23[d]={}
 for key in keys:
  if key==d: continue
  if len(c[key].keys())>1:
   k1=sorted(c[key].keys()); t1=0
   for t in k1:
    if isinstance(c[key][t],dict):
     k2=sorted(c[key][t].keys())
     for v in k2:
      lc='<%s %s="%s">'%(key,t,v); cnt=c[key][t][v]
      if lc not in c32.keys(): c32[lc]={}
      c23[d][lc]=cnt; c32[lc][d]=cnt; t1=t1+c[key][t][v]
    else: 
     if not t=="_cnt_": 
      lc='<%s %s>'%(key,t); cnt=c[key][t]
      if lc not in c32.keys(): c32[lc]={}
      c23[d][lc]=cnt; c32[lc][d]=cnt; t1=t1+c[key][t]
   if t1<>c[key]['_cnt_']:
    lc='<%s>'%(key); cnt=int(abs(c[key]['_cnt_']-t1))
    if lc not in c32.keys(): c32[lc]={}
    c23[d][lc]=cnt; c32[lc][d]=cnt
  else: 
   lc='<%s>'%(key); cnt=c[key]['_cnt_']
   if lc not in c32.keys(): c32[lc]={}
   c23[d][lc]=cnt; c32[lc][d]=cnt

def write_tags(fileout):
 outarr=[]; k23=sorted(c23.keys())
 for i in k23:
  k23d=sorted(c23[i].keys())
  for j in k23d:
   outarr.append('%06d %-04s %s'%(c23[i][j],i,j))
 with codecs.open("%s23.txt"%(fileout),'w','utf-8') as f:
  for out in outarr: f.write(out + '\n')
 outarr=[]; k32=sorted(c32.keys())
 for i in k32:
  k32d=sorted(c32[i].keys())
  for j in k32d:
   outarr.append('%06d %-04s %s'%(c32[i][j],j,i))
 with codecs.open("%s32.txt"%(fileout),'w','utf-8') as f:
  for out in outarr: f.write(out + '\n')
#-----------------------------------------------------
if __name__=="__main__":
 filedtd = sys.argv[1]
 fileout = sys.argv[2]
 with open(filedtd,"r") as f:
  for ln in f:
   if ln.startswith("<!ATTLIST"): 
    r=ln.split(); elt=r[1]; attr=r[2]
    if elt not in attrs: attrs[elt]={}
    if attr not in attrs[elt]: attrs[elt][attr]={}
    if "CDATA" not in ln: 
     for i in re.findall(r'\((.*?)\)',ln)[0].split('|'):
      attrs[elt][attr][i.lstrip().rstrip()]=1
 for dctn in ('acc','ae','ap','ap90','ben','bhs','bop','bor','bur','cae','ccs','gra','gst','ieg','inm','krm','mci','md','mw','mw72','mwe','pd','pe','pgn','pui','pw','pwg','sch','shs','skd','snp','stc','vcp','vei','wil','yat'):
  filexml="../../../%s/pywork/%s.xml"%(dctn,dctn)
  if os.path.exists(filexml):
   iter(objectify.parse(filexml).getroot()); sort_tags(dctn); c={}
 write_tags(fileout)
