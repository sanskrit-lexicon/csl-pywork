# coding=utf-8
""" generate.py
 07-18-2018
 09-21-2019 copied from csl-websanlexicon/v00.  
  includes 'D' option
 09-22-2019 includes 'CD' (copy distinct) option
 Also, inventory records now have 3 fields
 10-11-2019 Special logic so mako can handle pywork/make_xml.py.
"""
from __future__ import print_function
import sys,re
import codecs
import os.path,time
from shutil import copyfile
from dictparms import alldictparms,microversion
# use mako templates
from mako.template import Template
# Use string.Template for
import string  

def get_cologne_flag():
 path = os.path.abspath(__file__)  # full path of this file
 return path.startswith('/nfs/')

def current_mmddyyyy():
 gmtime = time.gmtime()  # current UTC time a 'time.struct_time' object
 year = gmtime.tm_year
 month = gmtime.tm_mon
 day = gmtime.tm_mday
 sfx = "%02d/%02d/%04d" %(month,day,year)
 return sfx

def get_directories(paths):
 """ Assume each path is NOT a directory.
  remove the filename (last component), to get directory part of path.
  Return list of distinct directories.
 """
 dirs = []
 for path in paths:
  dirname = os.path.dirname(path)
  #print('path=',path,'dirname=',dirname)
  if dirname not in dirs:
   dirs.append(dirname)
 return dirs

def makedirs(dirname,inventory):
 paths = ["%s/%s" % (dirname,filename_new) for 
          (category,filename_old,filename_new) in inventory]
 subdirs = get_directories(paths)
 #print('makedirs:',subdirs)
 for dirname in subdirs:
  try:
   os.makedirs(dirname)
  #except FileExistsError:  # requires Python 3.3+
  # ref: https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
  except:  #IOError:
   # directory already exists
   #print(dirname,'already exists')
   pass

def copyfiles(filenames,olddir,newdir):
 for filename in filenames:
  src = '%s/%s' %(olddir,filename)
  dst = '%s/%s' %(newdir,filename)
  copyfile(src,dst)
 #print(len(filenames),'copied from',olddir,'to',newdir)

def init_inventory_distinct(filein,dictcode):
 """
 # inventory. all paths assumed relative
 # generate inventory for this dictionary, based on the contents of
 # inventory of distinct files
 Format:  colon separated fields
  - dicts :  either 
     (a) the '*' character, meaning this file is for all dictionaries or
     (b) a space separated list of (lower-case) dictionary codes
  - path : a 'string template' with only 1 template variable possible, dictlo
  - category: currently, only 'C' (copy) is only category implemented
 Examples:
  1.  *:make_xml.py:C   means that file make_xml.py is in inventory for all dicts
  2. pw pwg:make_xml1.py:C  means the make_xml1.py is in inventory only for
     dictionaries pw and pwg
  3.  *:${dictlo}.dtd:C   means that xxx.dtd is in inventory for all dictionary
        codes xxx.
  11-04-2019  the 2nd parameter (filename) can have an old and new name
     space-delimited. e.g. *:${dictlo}.txt orig/${dictlo}.txt:CD
 """
 ans = []
 with codecs.open(filein,"r","utf-8") as f:
  for ix,x in enumerate(f):
   if x.startswith(';'): # comment
    continue 
   x = x.rstrip('\r\n')
   try:
    (dictcodes_str,filename_template_str,category) = x.split(':')
   except:
    print('ERROR parsing',filein,'at line',ix+1)
    print('line=',x)
    exit(1)
   # does our dictcode parameter match the dictcodes_str parameter?
   in_dictcode_inventory = False  
   if dictcodes_str == '*':
    in_dictcode_inventory = True
   else:
    dictcodes = dictcodes_str.split(' ')
    in_dictcode_inventory = dictcode in dictcodes
   if not in_dictcode_inventory:
    continue
   # Generate the filename from the template string
   filename_template = string.Template(filename_template_str)
   d = {'dictlo':dictcode}
   filename = filename_template.substitute(d)
   if ' ' in filename:
    # allow 'filename' to contain 2 values: old new
    filename_old,filename_new = re.split(' +',filename)
   else:
    filename_old = filename
    filename_new = filename 
   ans.append((category,filename_old,filename_new))
 if False:
  print('Generated inventory for',dictcode,'from input',filein)
  for (cat,filename_old,filename_new) in ans:
   print(cat,filename_old,filename_new)
 return ans

def expand_template(x,dictparms):
 t = string.Template(x)
 y = t.substitute(dictparms)
 if False:
  print('expand_template. x=',x,'y=',y)
 return y

def mako_preprocess(text):
 text1 = text.replace('<%s>','!!!s!!!')
 text1 = text1.replace('</%s>','!!!/s!!!')
 text1 = re.sub(r'^# coding=utf-8','!# coding=utf-8',text1)
 text1 = text1.replace('##','!!!##!!!')
 return text1

def mako_postprocess(text):
 text1 = text.replace('!!!s!!!','<%s>')
 text1 = text1.replace('!!!/s!!!','</%s>')
 text1 = re.sub(r'^!# coding=utf-8',r'# coding=utf-8',text1)
 text1 = text1.replace('!!!##!!!','##')
 return text1

def mako_special_handling(filein,dictparms):
 with codecs.open(filein,"r","utf-8") as f:
  text = f.read()
 text1 = mako_preprocess(text)
 template = Template(text1)
 renderedtext1 = template.render_unicode(**dictparms)
 renderedtext = mako_postprocess(renderedtext1)
 return renderedtext
if __name__=="__main__":
 dictcode = sys.argv[1]
 filein = sys.argv[2]  # inventory.txt
 olddir_template = sys.argv[3]  # makotemplates
 olddir1_template = sys.argv[4] # distinctfiles
 newdir_template = sys.argv[5]  # target directory
 dictcode = dictcode.lower() # Make case insensitive.
 dictparms = alldictparms[dictcode]
 # add dictmmddyyyy string 
 dictparms['dictmmddyyyy'] = current_mmddyyyy()
 # revise dictversion to include microversion
 dictparms['dictversion'] = dictparms['dictversion'] + microversion
 #print("Using dictversion=%s" %dictparms['dictversion'])
 # Add cologne flag  (used in redo_xml.sh for mw)
 dictparms['cologne_flag'] = get_cologne_flag()
 #
 inventory = init_inventory_distinct(filein,dictcode)
 olddir = expand_template(olddir_template,dictparms)
 olddir1 = expand_template(olddir1_template,dictparms)
 newdir = expand_template(newdir_template,dictparms)
 # make newdir directory, and needed subdirectories
 makedirs(newdir,inventory)
 # copy
 for category,filename_old,filename_new in inventory:
  if category == 'C':
   # just copy
   filename1 = "%s/%s" %(olddir,filename_old)
   newfile = "%s/%s" %(newdir,filename_new)
   copyfile(filename1,newfile)
  elif category == 'CD':
   # just copy distinct file from olddir1
   filename1 = "%s/%s" %(olddir1,filename_old)
   newfile = "%s/%s" %(newdir,filename_new)
   try:
    copyfile(filename1,newfile)
   except:
    print('generate.py. ERROR CD copyfile. filename1=%s, newfile=%s' %
          (filename1,newfile))
    exit(1)
  elif category == 'T':
   # process as a template
   filename1 = "%s/%s" %(olddir,filename_old)
   newfile = "%s/%s" %(newdir,filename_new)
   if filename_old != 'pywork/make_xml.py':
    template = Template(filename=filename1,input_encoding='utf-8',)
    renderedtext = template.render_unicode(**dictparms)
   else:
    renderedtext = mako_special_handling(filename1,dictparms)

   with codecs.open(newfile,"w","utf-8") as f:
    f.write(renderedtext)
  elif category == 'D':
   filename1 = "%s/%s" %(olddir,filename_old)
   newfile = "%s/%s" %(newdir,filename_new)
   if os.path.exists(newfile):
    os.remove(newfile)
   else:
    pass
    #print('WARNING: %s does not exist -- cannot delete'%newfile)
  else:
   print("unexpected inventory category:",category,filename)
   exit(1)

