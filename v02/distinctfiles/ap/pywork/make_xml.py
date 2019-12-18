# coding=utf-8
""" make_xml.py
 Reads/Writes utf-8
"""
from __future__ import print_function
import xml.etree.ElementTree as ET
import sys, re,codecs
from hwparse import init_hwrecs,HW
xmlroot = HW.dictcode  

def unused_adjust_slp1(x):
 # in vcp, all text is Devanagari.  But, the text is vcp.txt does not use
 #  the {#..#} markup to denote Devanagari.
 # We want to add <s>..</s> markup.
 # This requires that we separate out other markup  (always in form
 # <...>)
 outarr = []
 import string
 regex = r'(<[^>]+>)|(\[Page.*?\])|([^%s])' %string.printable
 parts = re.split(regex,x) 
 for part in parts: 
  if not part: #why needed? 
   pass 
  elif part.startswith('<') and part.endswith('>'):
   outarr.append(part)
  elif part.startswith('[Page') and part.endswith(']'):
   outarr.append(part)
 # elif part.startswith('&') and part.endswith(';'):
  elif part[0] not in string.printable:
   outarr.append(part)
  else: # assume text slp1
   # put it into <s></s>
   y = part
   outarr.append("<s>%s</s>" % y)
 ans = ''.join(outarr)
 return ans

def dig_to_xml_specific(x):
 """ changes particular to digitization"""
 # There is one instance of a 'Poem' tag, under hw=akzOhiRI
 #  <Poem>...
 #  ...
 #   ... </Poem>
 # change this to <div n="Poem">...</div>
 if re.search('Poem>',x):
  x = x.replace('<Poem>','<div n="Poem">')
  # Because of the the 'close_div' logic, we just remove </Poem>.
  # The close-div logic will add the </div>
  #x = x.replace('</Poem>','</div>')
  x = x.replace('</Poem>','')
  return x
 # in AP, ‡ is used in Devanagari text to indicate a line-break hyphen
 # This is different from the usage of this symbol in AP90.
 # Replace with '-'
 x = re.sub(u'‡','-',x) 
 # in ap.txt, the Currency symbol € is markup indicating a root. It has no
 # correspondent in the printed text. About 3000+ instances.
 # For now, replace it with an empty '<root/>' element, and do not display
 # it in 'disp.php'
 x = x.replace(u'€','<root/>')
 # Divisions are indicated by lines starting with a period.
 # Three types are seen:
 # .{#-BaH#}   
 # .²1 Absence  ...
 # .³({%a%})    
 if re.search(u'^[.][²]',x):
 # there may be nothing else on the line (300+ cases), in particular no space
 # do same thing anyway, not requiring the trailing space.
  x = re.sub(u'[.][²]([^ ]*) ',r'<div n="2" name="\1">\1 ',x)
  x = re.sub(u'[.][²]([^ ]*)',r'<div n="2" name="\1">\1 ',x)
 elif re.search(u'^[.][³]',x):
  m = re.search('[.][³]([^ ]*) ',x)
  if not m:
   m = re.search('[.][³]([^ ]*)',x)
  assert m ,"adjust_xml. PROBLEM 1:x=\n%s"%x.encode('utf-8')
  data = m.group(1)
  # data = ({%x%})
  m = re.search(r'\(<i>(.)</i>\)',data)
  assert m ,"adjust_xml. PROBLEM 2:x=\n%s"%x.encode('utf-8')
  name=m.group(1)
  x = re.sub(u'[.][³]([^ ]*) ',r'<div n="3" name="%s">\1 '%name,x)
  x = re.sub(u'[.][³]([^ ]*)',r'<div n="3" name="%s">\1 '%name,x)

 # introduce line-break (call it a plain div) at any line starting with
 # a period.  This was the convention used by Thomas to designate
 # divisions. This is the /{#-BaH#} type case
 if x.startswith('.'):
  #print("extra div:",x.encode('utf-8'))
  x = re.sub(r'^[.]','<div n="?">',x)
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
 """ line is the full xml record, but the <div> elements have not been
  closed.  Don't close empty div tags.
 """
 divregex = r'<div[^>]*?[^/]>'
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
 nerr = 0
 for ihwrec,hwrec in enumerate(hwrecs):
  if ihwrec > 1000000: # 12 
   print("debug stopping")
   break
  datalines = get_datalines(hwrec,inlines)
  # construct output
  xmlstring = construct_xmlstring(datalines,hwrec)
  # data is a string, which should be well-formed xml
  # try parsing this string to verify well-formed.
  try:
   root = ET.fromstring(xmlstring.encode('utf-8'))
  except:
   outarr = []
   nerr = nerr + 1
   out = "<!-- xml error #%s: L = %s, hw = %s-->" %(nerr,hwrec.L,hwrec.k1)
   outarr.append(out)
   outarr.append("datalines = ")
   outarr = outarr + datalines
   outarr.append("xmlstring=")
   outarr.append(xmlstring)
   outarr.append('')
   for out in outarr:
    print(out.encode('utf-8'))
   #exit(1) continue
  # write output
  fout.write(xmlstring + '\n')
  nout = nout + 1

 # write closing line for xml file.
 out = "</%s>\n" % xmlroot
 fout.write(out)
 fout.close()

if __name__=="__main__":
 filein = sys.argv[1] # xxx.txt
 filein1 = sys.argv[2] #xxxhw2.txt
 fileout = sys.argv[3] # xxx.xml
 make_xml(filein,filein1,fileout)
