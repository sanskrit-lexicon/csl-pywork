# coding=utf-8
""" make_xml.py for  2014-06-10
 Reads/Writes utf-8
 Mar 12, 2015
 Remove conversion of HK to SLP1 - See convertwork/readme.txt
 05-03-2017  <HI1> -> <div n="2">...</div>
 05-31-2017  Revise to use new forms digitization and headwords.
"""
import xml.etree.ElementTree as ET
import sys, re,codecs
from hwparse import init_hwrecs,HW
xmlroot = HW.dictcode  

def dig_to_xml_specific(x):
 """ changes particular to sch digitization"""
 # 04-24-2017.  Several changes
 # {!x!}  a pw homonym number
 x = re.sub(r'{!(.%?)!}',r'<hom n="pwk">\1</hom>',x)
 # {part=,seq=6766,type=,n=5}
 m = re.search(r'{part=(.*?),seq=(.*?),type=(.*?),n=(.*?)}',x)
 if m:
  temp = m.group(0)
  part = m.group(1)
  seq = m.group(2)
  t = m.group(3) # type
  n = m.group(4)
  if t != '':
   telt = '<type>%s</type>'% t
  else:
   telt = ''
  attribs=[]
  attribs.append('seq="%s"'%seq)
  attribs.append('n="%s"' %n)
  if part != '':
   attribs.append('part="%s"' % part)
  attribstr = ' '.join(attribs)
  infoelt = '<info %s/>' %attribstr
  new = '%s%s' %(telt,infoelt)
  #new = '<info part="%s" seq="%s" n="%s"/><type>%s</type>'%(part,seq,n,t)
  x = x.replace(temp,new)
 # introduce '<div>' before each EM DASH
 x = x.replace(u'—',u'<div>—')
 return x

def dig_to_xml_general(x):
 """ These changes likely apply to ALL digitizations"""
 # xml requires that an ampersand be represented by &amp; entity
 x = x.replace('&','&amp;')
 # remove broken bar.  In xxx.txt, this usu. indicates a headword end
 x = x.replace(u'¦',' ') 
 # bold, italic, and Sanskrit markup converted to xml forms.
 x = re.sub(r'{@','<b>',x)
 x = re.sub(r'@}','</b>',x)
 x = re.sub(r'{%','<i>',x)
 x = re.sub(r'%}','</i>',x)
 x = re.sub(r'{#','<s>',x)
 x = re.sub(r'#}','</s>',x)
 return x

def dig_to_xml(xin):
 x = xin
 x = dig_to_xml_general(x)
 x = dig_to_xml_specific(x)
 return x

def dbgout(dbg,s):
 if not dbg:
  return
 filedbg = "make_xml_dbg.txt"
 fout = codecs.open(filedbhg,"a","utf-8")
 fout.write(s + '\n')
 fout.close()

def close_divs(line):
 """ line is the full xml record, but the '<div> elements have not been
  closed.  
 """
 divregex = r'<div.*?>'
 if not re.search(divregex,line):
  # no divs to close
  return line
 ans = [] # strings parts of data
 idx0 = 0
 # div can have attribute
 for m in re.finditer(divregex,line): 
   idx1=m.start()
   idx2 = m.end()
   line1 = line[idx0:idx1] # text preceding this div
   ans.append(line1)
   if idx0 != 0: 
    # close the previous div
    ans.append('</div>')
   # include this div
   linediv = line[idx1:idx2]
   ans.append(linediv)
   idx0 = idx2 # reset for next iteration
 # construct string for all text in line upto position idx0
 new = ''.join(ans) 
 # The last div will not be closed
 rest = line[idx0:]  
 # We can assume that rest contains 
 # <type>*</type></body> -> </div><type>*</type></body>
 # (no type)</body> -> </div></body>
 if re.search(r'(<type>.*?</type>)</body>',rest):
  newrest = re.sub(r'<type>',r'</div><type>',rest)
 elif re.search(r'</body>',rest):
  newrest = re.sub(r'</body>','</div></body>',rest)
 else:
  raise ValueError("close_divs_error: %s"%line.encode('utf-8'))
 newline = new + newrest
 return newline

def construct_xmlhead(hwrec):
 key2 = hwrec.k2
 key1 = hwrec.k1
 hom = hwrec.h
 if hom == None:
  # no homonym
  h = "<key1>%s</key1><key2>%s</key2>" % (key1,key2)
 else:
  h = "<key1>%s</key1><key2>%s</key2><hom>%s</hom>" % (key1,key2,hom)
 return h

def construct_xmltail(hwrec):
 L = hwrec.L
 pagecol = hwrec.pc
 tail = "<L>%s</L><pc>%s</pc>" % (L,pagecol)
 if hwrec.type == None:
  # normal
  return tail
 # otherwise, also <hwtype n="type" ref="LP"
 hwtype = '<hwtype n="%s" ref="%s"/>' %(hwrec.type,hwrec.LP)
 tail = tail + hwtype
 return tail

def body_alt(bodylines,hwrec):
 """
  insert an extra body line at the top.
 """
 hwtype = hwrec.type
 assert hwtype in ['alt','sub'],"body_alt error: %s"%hwtype
 LP = hwrec.LP  # L-number of parent
 hwrecP = HW.Ldict[LP]
 key1P = hwrecP.k1
 key1 = hwrec.k1
 templates = {
  'alt':'<alt>%s is an alternate of %s.</alt>',
  'sub':'<alt>%s is a sub-headword of %s.</alt>'
 }
 if HW.Sanskrit:
  # prepare for conversion from slp1 to user choice
  key1P = '<s>%s</s>' %key1P
  key1 = '<s>%s</s>' %key1
 template = templates[hwtype]
 extraline = template %(key1,key1P)
 # insert extraline at the front
 return [extraline]+bodylines

def construct_xmlstring(datalines,hwrec):
 dbg = False
 datalines1 = []
 # 1. h (head)
 h = construct_xmlhead(hwrec)
 dbgout(dbg,"head: %s" % h)  
 #2. construct tail
 tail = construct_xmltail(hwrec)
 dbgout(dbg,"tail: %s" % tail)  
 #3. construct body
 # To mimic current display of Sch, we remove the 'head' from first line:
 datalines1=[]
 for i,x in enumerate(datalines):
  if i == 0:
   m = re.search(u'^(.*?¦)(.*)$' ,x)
   if not m:
    print "xml_string ERROR at =",x.encode('utf-8')
    exit(1)
   head = m.group(1)
   rest = m.group(2)
   x = rest
  datalines1.append(x)
 datalines = datalines1
 bodylines = [dig_to_xml(x) for x in datalines]
 if hwrec.type != None:
  bodylines = body_alt(bodylines,hwrec)
 body0 = ' '.join(bodylines)
 dbgout(dbg,"chk4: %s" % body0)
 body = body0
 dbgout(dbg,"body0: %s" % body0)
 ##3a. Remove <LEND>. datalines does not include <LEND>. See get_datalines
 #body = body.replace('<LEND>','') # Line ending mark needs to be removed.
 #4. construct result
 data = "<H1><h>%s</h><body>%s</body><tail>%s</tail></H1>" % (h,body,tail)
 #4a. For sch: Put the <info> element into the tail
 data = re.sub('(<info.*?>) *</body><tail>',r'</body><tail>\1',data)
 #4b. For comparison to previous version, remove a space after <body>
 data = re.sub(r'<body> ','<body>',data)
 #5. Close the <div> elements
 data = close_divs(data)
 return data

def xml_header(xmlroot):
 # write header lines
 text = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE %s SYSTEM "%s.dtd">
<!-- Copyright Universitat Koln 2013 -->
<%s>
""" % (xmlroot,xmlroot,xmlroot)
 lines = text.splitlines()
 lines = [x.strip() for x in lines if x.strip()!='']
 return lines

def get_datalines(hwrec,inlines):
 # for structure of hwrec, refer to hwparse.py
 n1 = int(hwrec.ln1)
 n2 = int(hwrec.ln2)
 # By construction, n1 is the meta line, and n2 is the <lend> line of
 # this entry in xxx.txt.
 # For our purposes, we do not need this first and last line
 n1 = n1 + 1
 n2 = n2 - 1
 # Next, we make indexes into the inlines array, which are 0-based
 # whereas n1 and n2 are 1-based
 idx1 = n1 - 1
 idx2 = n2 - 1
 datalines = inlines[idx1:idx2+1]
 return datalines

def make_xml(filedig,filehw,fileout):
 # slurp txt file into list of lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
    inlines = [line.rstrip('\r\n') for line in f]
 # parse xxxhw.txt 
 hwrecs = init_hwrecs(filehw)
 # open output xml file
 fout = codecs.open(fileout,'w','utf-8')
 nout = 0  # count of lines written to fout
 # generate xml header lines
 lines = xml_header(xmlroot)
 for line in lines:
  fout.write(line + '\n')
  nout = nout + 1
 # process hwrecs records one at a time and generate output
 for ihwrec,hwrec in enumerate(hwrecs):
  if ihwrec > 1000000: # 12 
   print "debug stopping"
   break
  datalines = get_datalines(hwrec,inlines)
  # construct output
  xmlstring = construct_xmlstring(datalines,hwrec)
  # data is a string, which should be well-formed xml
  # try parsing this string to verify well-formed.
  try:
   root = ET.fromstring(xmlstring.encode('utf-8'))
  except:
   out = "xml error: n=%s,m line=\n%s\n" %(nout+1,xmlstring)
   print out.encode('utf-8')
   exit(1)
  # write output
  fout.write(xmlstring + '\n')
  nout = nout + 1

 # write closing line for xml file.
 out = "</%s>\n" % xmlroot
 fout.write(out)
 fout.close()

if __name__=="__main__":
 filein = sys.argv[1] # acc.txt
 filein1 = sys.argv[2] #acchw2.txt
 fileout = sys.argv[3] # acc.xml
 make_xml(filein,filein1,fileout)
