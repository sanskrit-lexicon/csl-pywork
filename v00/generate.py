# coding=utf-8
""" generate.py
 07-18-2018
  
"""
from __future__ import print_function
import sys,re
import codecs
import os.path,time
from shutil import copyfile
from dictparms import alldictparms,microversion
# use mako templates
from mako.template import Template

def current_mmddyyyy():
 gmtime = time.gmtime()  # current UTC time a 'time.struct_time' object
 year = gmtime.tm_year
 month = gmtime.tm_mon
 day = gmtime.tm_mday
 sfx = "%02d/%02d/%04d" %(month,day,year)
 return sfx

def makedirs(webdirname):
 if not os.path.exists(webdirname):
  os.makedirs(webdirname)
 else:
  print('makedirs WARNING: target directory already exists:',webdirname)
  return
 subdirs = []
 for subdir in subdirs:
  os.makedirs('%s/%s' %(webdirname,subdir))

def copyfiles(filenames,olddir,newdir):
 for filename in filenames:
  src = '%s/%s' %(olddir,filename)
  dst = '%s/%s' %(newdir,filename)
  copyfile(src,dst)
 print(len(filenames),'copied from',olddir,'to',newdir)

def init_inventory(filein):
 # read inventory. all paths assumed relative
 ans = []
 with codecs.open(filein,"r","utf-8") as f:
  for x in f:
   if x.startswith(';'): # comment
    continue 
   x = x.rstrip('\r\n')
   (filename,category) = x.split(':')
   ans.append((category,filename))
 return ans
if __name__=="__main__":
 dictcode = sys.argv[1]
 dictcode = dictcode.lower() # Make it case insensitive
 filein = sys.argv[2]  # inventory
 oldweb = sys.argv[3]  # "templates"
 newweb = sys.argv[4]
 # make newweb directory, and needed subdirectories
 makedirs(newweb)
 dictparms = alldictparms[dictcode]
 # add dictmmddyyyy string 
 dictparms['dictmmddyyyy'] = current_mmddyyyy()
 # revise dictwebversion to include microversion
 dictparms['dictwebversion'] = dictparms['dictwebversion'] + microversion
 print("Using dictwebversion=%s" %dictparms['dictwebversion'])
 inventory = init_inventory(filein)
 # copy
 for category,filename in inventory:
  filename1 = "%s/%s" %(oldweb,filename)
  newfile = "%s/%s" %(newweb,filename)
  if category == 'C':
   # just copy
   copyfile(filename1,newfile)
  elif category == 'T':
   # process as a template
   template = Template(filename=filename1,input_encoding='utf-8',)
   renderedtext = template.render_unicode(**dictparms)
   with codecs.open(newfile,"w","utf-8") as f:
    f.write(renderedtext)
  else:
   print("unexpected inventory category:",category,filename)
   exit(1)

