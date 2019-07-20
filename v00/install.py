# coding=utf-8
""" install.py
 Jul 4, 2018
  
"""
import sys,re
import codecs
import os.path,time
import shutil
from dictparms import alldictparms
# use mako templates
from mako.template import Template


def copyfiles(filenames,olddir,newdir):
 for filename in filenames:
  src = '%s/%s' %(olddir,filename)
  dst = '%s/%s' %(newdir,filename)
  copyfile(src,dst)
 print(len(filenames),'copied from',olddir,'to',newdir)


def movedatafiles(statusFlag,dictcode):
 # these are moved from a copy of the previous version.
 movefilenames = [
  'pdfpages',  # scanned images
  'fonts',     # siddhanta, perhaps other fonts.
  '%sheader.xml'%dictcode,
  'index.php',
  'readme.txt',
  'sqlite/%s.sqlite'%dictcode,
  'sqlite/%sab.sqlite'%dictcode,
  #'sqlite/%sauth.sqlite'%dictcode,
  #'webtc2/query_dump.txt',   # removed 07-08-2018
  'webtc/pdffiles.txt',
 ]
 if dictcode == 'pwg':
  extrafilenames=['sqlite/%sbib.sqlite'%dictcode,]
 elif dictcode == 'mw':
  extrafilenames=['sqlite/%sauthtooltips.sqlite'%dictcode,]

 else:
  extrafilenames=[]
 movefilenames = movefilenames + extrafilenames

 movepairs = []
 for filename in movefilenames:
  src = '%s/%s' %(savewebpath,filename)
  dst = '%s/%s' %(webpath,filename)
  movepairs.append((src,dst))

 for src,dst in movepairs:
  if os.path.exists(src) and statusFlag:
   print "mv %s %s" %(src,dst)
   shutil.move(src,dst)
  else:
   print "# TODO: mv %s %s" %(src,dst)
 
 # reminder on query_dump
 filename="webtc2/query_dump.txt"
 src = '%s/%s' %(savewebpath,filename)
 dst = '%s/%s' %(webpath,filename)
 print "REMINDER on %s:" % dst
 print "  a) cd %s/webtc2" %webpath
 print "  b) sh init_query.sh"

def savewebname(webpath):
 # time of last modification.
 mtime = os.path.getmtime(webpath)
 gmtime = time.gmtime(mtime)  # UTC time a 'time.struct_time' object
 year = gmtime.tm_year
 month = gmtime.tm_mon
 day = gmtime.tm_mday
 h = gmtime.tm_hour
 m = gmtime.tm_min
 s = gmtime.tm_sec
 sfx = "%04d%02d%02d" %(year,month,day)
 webpathnew = "%s_%s" %(webpath,sfx)
 if os.path.exists(webpathnew):
  # add a letter suffix. Fail if all are found (surely won't happen)
  import string
  found = False
  for letter in string.ascii_lowercase:
   w = "%s%s" %(webpathnew,letter)
   if not os.path.exists(w):
    webpathnew = w
    found = True
    break
  if not found:
   print "ERROR savewebname: cannot find new name for",webpath
   exit(1)
 return webpathnew

if __name__=="__main__":
 dictcode = sys.argv[1]
 webnew = sys.argv[2]  # The version to install
 oldwebparent = sys.argv[3]  # path to the parent. Where to install.
 # name of folder where we will move {oldwebparent}/web
 webpath = "%s/web" % oldwebparent
 savewebpath = savewebname(webpath)
 print "rename %s as %s"%(webpath,savewebpath)
 # rename webpath to savewebpath
 os.rename(webpath,savewebpath)
 # rename webnew to webpath
 print "rename %s as %s"%(webnew,webpath)
 try:
  os.rename(webnew,webpath)
  webpathok = True
 except Exception as e:
  print "ERROR in rename %s as %s"%(webnew,webpath)
  webpathok = False
 movedatafiles(webpathok,dictcode)

 
