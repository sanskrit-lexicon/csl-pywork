# coding=utf-8
""" init_query.py 
 Reads/Writes utf-8
 Jul 6, 2018:  A conversion to Python of init_query.php.
 Python2 syntax.
 init_query.php was not properly handling extended ascii characters.
// create query_dump.txt from xml file (generic)
// modified to included embedded sanskrit, which is converted to slp
  
"""
from __future__ import print_function
import sys, re,codecs

def make(filein,fileout):
 fp = codecs.open(filein,"r","utf-8")
 fpout = codecs.open(fileout,"w","utf-8")

 n=0;
 prevkey='';
 lnum1=0;
 nfound=0;
 nfound1=0;
 prevkey="";
 key='';
 keydata="";

 for line in fp:
  line = line.rstrip('\r\n')

  m = (re.search(r'^<H.*?<key1>(.*?)</key1>.*<body>(.*?)</body>.*<L.*?>(.*?)</L>',line))
  if m:
   n = n + 1
   key=m.group(1)
   body = m.group(2)
   L=m.group(3)
   data1 = query_line(body)
   data2 = query_sanskrit(body)
   #data2 = "" # currently, no good way to distinguish Sanskrit words.
   ## if prevkey is empty, start a new keydata
   ## else if a new key, output keydata
   ## else append data1 to keydata
   if (prevkey == "") :
     prevkey = key
     keydata = data1
     keysanskrit = data2
   elif (prevkey == key):
     keydata += " :: %s" % data1
     keysanskrit += " :: %s" % data2
   else:
     fpout.write('%s :: %s\t%s\n' %(prevkey,keysanskrit,keydata))
     nfound1 = nfound1 + 1
     prevkey = key
     keydata = data1
     keysanskrit = data2

 # print last one
 fpout.write('%s :: %s\t%s\n' %(prevkey,keysanskrit,keydata))
 fpout.write("prevkey :: keysanskrit\tkeydata\n")
 fp.close()
 fpout.close()

 print(n,"records read from",filein)
 print(nfound1,"records written to",fileout)

def query_line(x):
 # see construction in make_xml.php for some details

 # (b) English can appear in italics
 #x = preg_replace('|\{%.*?%\}|','',x)
 #x = preg_replace('|\{@.*?@\}|','',x)

 # (c) Remove markup
 x =re.sub(r'<s>.*?</s>','',x) # remove embedded SLP sanskrit
 x = re.sub('<.*?>',' ',x)
 #x = preg_replace('|\{#.*?#\}|','',x) # A few sanskrit letters coded as HK
 

 # (d) Remove punctuation
 x = re.sub('\[Page.*?\]','',x)
 x = re.sub('[~_;., ?()\[\]]+',' ',x)
 # (e) downcase
 x = x.lower()
 
 # (f) replace AS codes (remove the number)
 x = re.sub("[0-9]","",x)
 return x

def query_sanskrit(x):
 sanwords = []
 # Get all the <s>x</s> words
 # The subroutine modifies sanwords
 parts = re.split(r'(<s>.*?</s>)',x)
 for part in parts:
  m = re.search('^<s>(.*?)</s>$',part)
  if m:
   subpart = m.group(1)
   subwords = query_sanskrit_helper1(subpart)
   sanwords = sanwords + subwords
 ans = ' '.join(sanwords)
 return ans

def query_sanskrit_helper1(s):
 # remove xml markup
 s = re.sub(r'<([^> ]*).*?>.*?</\1>',' ',s)
 s = re.sub('<.*?>',' ',s)
 # remove extended ascii, which is coded as html entity: &...;
 #s = re.sub('|&.*?;|',' ',s)
 # remove slp accent chars, if present
 s = re.sub(r'[/\\~^]','',s)
 words = re.split("[^a-zA-Z|']",s)
 return words


if __name__=="__main__":
 filein = sys.argv[1] # xxx.xml
 fileout = sys.argv[2] # query_dump
 make(filein,fileout)
