# coding=utf-8
""" make_xml.py for ben. 2014-03-24
 Reads/Writes utf-8
 Nov 8, 2014. No transcoding to SLP1 required.
"""
import xml.etree.ElementTree as ET
import sys, re,codecs
import transcoder
transcoder.transcoder_set_dir("");
xmlroot = "ben"
import headword
reHeadword0 = headword.reHeadword
reHeadword = re.compile(reHeadword0)
reHeadworda0 = headword.reHeadworda  # usual case where key2 visible
reHeadworda = re.compile(reHeadworda0)

def adjust_tag(x,j):
 # see check_tags
 x = re.sub(r'<>','<lb/>',x) # beginning of normal line
 x = re.sub(r'<P>','<P/>',x) # beginning of headword line
 #x = re.sub(r'<g>.*</g>','',x) # beginning of headword line
 x = re.sub(r'<HI>','',x) # used in Additions and Corrections only
 x = re.sub(r'<NI>','',x) # used once in Preface
 x = re.sub(r'<H>.*$','',x) # Section separators (as at beg. of letter section)
 return x
def add_tag(x,j):
 # compare to check_curly
 x = re.sub(r'{%','<i>',x) 
 x = re.sub(r'%}','</i>',x)
 x = re.sub(r'{@','<b>',x) 
 x = re.sub(r'@}','</b>',x)
 x = re.sub(r'{#','<s>',x)
 x = re.sub(r'#}','</s>',x)
 x = re.sub(r'{[?]+}','??',x) # unreadable
 x = re.sub(r'{|','',x) #this and next in one line only.
 x = re.sub(r'|}','',x) 
 #x = re.sub(r'{kh}','<kh/>',x)
 #x = re.sub(r'{greek}','<greek/>',x)
 return x

def unused_adjust_hk(m):
 x = m.group(1)
 # re.split(r'(<[^>]+>)',s)(&.*;)
 outarr = []
 parts = re.split(r'(<[^>]+>)',x) # xml tags
 for part in parts: 
  if (part == ''):
   pass
  elif (part[0] == '<'):
   outarr.append(part)
  else:
   parts1 = re.split(r'(&.*;)',part) # xml entity
   for part1 in parts1:
    if (part1 == ''):
     pass
    elif (part1[0] == '&'):
     outarr.append(part1)
    else: # assume text in hk. Convert to slp1
     z = re.sub(r'\|','.',part1) # text has non-standard | for danda
     if z == 'oMM':
      y = 'o~' # OM
     else:
      y = transcoder.transcoder_processString(z,'hk','slp1')
     outarr.append(y)
 ans = ''.join(outarr)
 return "<s>%s</s>" % ans

def dbgout(fout,s):
 if fout:
  fout.write("%s\n" % s)

def construct_data(datalines,key1,lnum,page,col,n1,fout=None):
 # construct data analogous to the way it is in mw
 # replace extended ascii in all lines
 datalines1 = []
 # parse head info from first line
 line = datalines[0]
 line = line.strip()
 line0 = line
 dbgout(fout,"chk1: %s\n" % line)
 m = re.search(r'^(.*?¦)(.*)$' ,line)  # may need vertical-bar
 if not m:
  print "CONSTRUCT_DATA ERROR at n1=",n1
  exit(1)
 head = m.group(1)
 rest = m.group(2)
 parts = [head,rest]
 if len(parts) == 2: # the usual case
  (head,rest) = parts
 elif len(parts) > 2: # occasional miscoding
  head = parts[0]
  xparts = [p.encode('utf-8') for p in parts]
  rest = r'¦'.join(xparts[1:])
  out = "WARNING: too many parts. line %s=\n%s" % (n1,line)
  print out.encode('utf-8')
  #exit(1)
 else:  # 1 part (no Â¦)
  print "ERROR: no head. line = \n%s\n" % line
  exit(1)
 #head = u"¦".join([head,''])
 m = re.search(reHeadworda,head)  
 if  m:
  hkey1a = m.group(1) # unused
  hkey2a = m.group(2) 
 else:
  hkey2a = key1
 hom = ''
 #key2a = transcoder.transcoder_processString(hkey2a,'hk','slp1')
 key2a = hkey2a # in AS encoding
 datalines[0] = rest
 for line in datalines:
  line = line.strip()
  if line == '':
   continue  # skip blank line
  # change & to &amp; for xml conformity
  line = re.sub('&','&amp;',line)
  datalines1.append(line)
 # 1. h (head)
 key2 = key2a  #adjust_key2(key2a)
 hom0=hom
 hom = re.sub(r'^[,.;^]+','',hom)
 hom = re.sub(r'[.]','',hom)
 hom = re.sub(r'[()]','',hom)
 m=re.search(r'^([0-9]+)$',hom)
 if (hom == ''):  # this is the case for ben
  h = "<key1>%s</key1><key2>%s</key2>" % (key1,key2)
 elif m:
  hom = m.group(1)
  h = "<key1>%s</key1><key2>%s</key2><hom>%s</hom>" % (key1,key2,hom)
 elif hom in ['I','II','III']:
  h = "<key1>%s</key1><key2>%s</key2><hom>%s</hom>" % (key1,key2,hom)
 else:
  h = "<key1>%s</key1><key2>%s</key2><hom>%s</hom>" % (key1,key2,hom)
  print "WARNING: odd hom='%s', hom0='%s',  line=\n%s" % (hom,hom0,line0)
 dbgout(fout,"chk2: %s" % h)  
 #2. construct tail
 #ipage = int(page)
 ipage = page
 tail = "<L>%s</L><pc>%s</pc>" % (lnum,ipage)
 dbgout(fout,"chk3: %s\n" % tail)  
 #3. construct body
 bodylines = []
 j = n1
 for x in datalines1:
  x = x.strip()
  #if re.search(r'<H>',x):
  # continue
  x = adjust_tag(x,j) # j not used here
  x = add_tag(x,j)
  # convert <s>X</s> to slp1  AUG 2013. Do this after lines are joined!
  #x = re.sub(r'<s>(.*?)</s>',adjust_hk,x)
  j = j + 1
  dbgout(fout,"chk3: %s" % x)
  bodylines.append(x)
 body0 = ' '.join(bodylines)
 dbgout(fout,"chk4: %s" % body0)
 # convert HK 'Sanskrit' to slp1: 
 # Nov 8, 2014. Sanskrit already is slp1. No adjustment needed
 #body = re.sub(r'<s>(.*?)</s>',adjust_hk,body0)
 body = body0
 dbgout(fout,"chk5: %s" % body0)
 #4. construct result
 data = "<H1><h>%s</h><body>%s</body><tail>%s</tail></H1>" % (h,body,tail)
 dbgout(fout,"chk6: %s" % body0)
 return data

def make_xmlfun(filein,filein1,fileout):
 # slurp txt file into list of lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
    inlines = f.readlines()
 # open output xml file, and write header
 fout = codecs.open(fileout,'w','utf-8')
  
 # write header lines
# write the preface pages
 text = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE %s SYSTEM "%s.dtd">
<!-- Copyright Universitat Koln 2013 -->
<%s>
""" % (xmlroot,xmlroot,xmlroot)
 lines = text.splitlines()
 nout = 0  # count of lines written
 for line in lines:
  line = line.strip()
  if (line != ''):
   out = "%s\n" %line
   fout.write(out)
   nout = nout + 1
 # read headword lines, and generate output
 f = open(filein1,'r')
 n = 0 # count of lines read
 lnum = 0 # generate record number for xml records constructed
 for line in f:
  n = n+1
  if n > 1000000:
   print "debug stopping"
   break
  line = line.strip() # remove starting or ending whitespace
  try:
   (pagecol,hwslp,linenum12) = re.split('[:]',line)
  except:
   print "Problem at line %s = %s" %(n,line)
   exit(1)
  (linenum1,linenum2) = re.split(',',linenum12)
  (page,col) = re.split('[-]',pagecol)  # - used for ben
  #col = 1 # there is no column for pd. 
  n1 = int(linenum1) - 1 # make 0-based
  n2 = int(linenum2) - 1
  datalines = inlines[n1:n2+1]
  # construct output
  lnum = lnum + 1
  key1 = hwslp
  # Mar 20, 2014. Display pagecol.
  #data = construct_data(datalines,key1,lnum,page,col,n1,fout=None)
  data = construct_data(datalines,key1,lnum,pagecol,col,n1,fout=None)
  out = "%s\n" % data
  try:
   fout.write( out)
  except:
   out1 = "ERROR WRITING line# %s" % n1
   print out1
   exit(1)
  # check that out is well-formed xml
  try:
   root = ET.fromstring(out.encode('utf-8'))
  except:
   out = "xml error: n=%s,line=%s" %(n,out)
   print out.encode('utf-8')
 # write closing line
 out = "</%s>\n" % xmlroot
 fout.write(out)
 fout.close()

if __name__=="__main__":
 filein = sys.argv[1] # ben.txt
 filein1 = sys.argv[2] #benhw2.txt
 fileout = sys.argv[3] # ben.xml
 make_xmlfun(filein,filein1,fileout)
