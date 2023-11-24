""" sqlite.py
   12-16-2020 ejf
   Create xxx.sqlite from xxx.xml
"""
from __future__ import print_function
import sys,re,codecs;
import sqlite3
import time  # for performance checks
def remove(fileout):
 import os
 if os.path.exists(fileout):
  os.remove(fileout)
  print("removed previous",fileout)

def get_dict_code(fileout):
 # assume fileout is xxx.sqlite
 m = re.search(r'^(.*?)[.]sqlite$',fileout)
 if not m:
  print('sqlite.py ERROR: cannot get dictionary code')
  print('fileout=',fileout)
  exit(1)
 code = m.group(1).lower() # should be lower case?
 print('sqlite.py: dictionary code=',code)
 return code

def create_table(c,conn,dictlo):
%if dictlo in ['abch']:
 template = '''
CREATE TABLE %s (
 key VARCHAR(100)  NOT NULL,
 lnum DECIMAL(10,2) NOT NULL,
 data TEXT NOT NULL
);
  ''' % dictlo
%else:
 template = '''
CREATE TABLE %s (
 key VARCHAR(100)  NOT NULL,
 lnum DECIMAL(10,2) UNIQUE,
 data TEXT NOT NULL
);
  ''' % dictlo
%endif
 if False:  #dbg
  print('DBG: table template=')
  print(template)
 c.execute(template)
 conn.commit()

def create_index(c,conn,tabname):
 time0 = time.time()
 sqls = [
  'CREATE INDEX datum on %s(key)',
  'pragma table_info (%s)',
  'select count(*) from %s'
 ]
 for sql in sqls:
  sql1 = sql % tabname
  c.execute(sql1)
  conn.commit()
 time1 = time.time()
 timediff = time1 - time0
 print('create_index takes %0.2f seconds' %timediff)

def insert_batch(c,conn,tabname,rows):
 # rows is a list.
 # if rows is empty, nothing to do
 if len(rows) == 0:
  return
 # 3 columns -> three placeholders (?)
 sql = 'INSERT INTO %s VALUES (?,?,?)' % tabname
 c.executemany(sql,rows)
 conn.commit()

%if dictlo in ['abch']:
def sort_lines(lines):
 slp_from = "aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
 slp_to =   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
 slp_from_to = str.maketrans(slp_from,slp_to)
 # filter, and generate sortkey
 rows = []
 for line in lines:
  if not line.startswith('<H'):
   # skip othere xml lines
   continue
  m = re.search(r'<key1>(.*?)</key1>.*<L>(.*?)</L>',line)
  if not m:
   print('ERROR: Could not find key1,lnum from line: %s' %line)
   exit(1)
  key1 = m.group(1)
  lnum = m.group(2)
  keysort = key1.translate(slp_from_to)  
  row = (keysort,key1,lnum,line)
  rows.append(row)
 # sort the rows
 rows1 = sorted(rows,key = lambda row: row[0])
 if False: # dbg print the sorted records
  fileout = 'temp_sqlite.txt'
  print('debug written to',fileout)
  with codecs.open(fileout,"w","utf-8") as f:
   for irow,row in enumerate(rows1):
    if (irow in [0,1]):
     f.write('%s %s %s %s\n' % row)
    else:
     f.write('%s %s %s\n' %(irow,row[0],row[1]))
            
 # remove the keysort field
 rows2 = [row[1:] for row in rows1]
 return rows2
%endif

if __name__ == "__main__":
 time0 = time.time() # a real number

 filein = sys.argv[1]   # xxx.xml
 fileout = sys.argv[2]  # xxx.sqlite
 if len(sys.argv) > 3:
  mbatch = int(sys.argv[3])
 else:
  # default batch size. 
  # experiments with Wilson shows 10000 is about maximal for time.
  # it is also not that big regarding memory.
  mbatch = 10000 
 remove(fileout) 
 # infer dictionary name from fileout
 dictlo = get_dict_code(fileout)
 # establish connection to xxx.sqlite, 
 # also creates xxx.sqlite if it doesn't exist
 conn = sqlite3.connect(fileout)
 c = conn.cursor()  # prepare cursor for further use
 # create the 'dictlo' table in db
 create_table(c,conn,dictlo)
 
 with codecs.open(filein,"r","utf-8") as f:
  lines = [line.rstrip('\r\n') for line in f]
  print(len(lines),'lines read from',filein)

%if dictlo in ['abch']:
 rows = sort_lines(lines)
 nrow = len(rows)
 batch = []
 for irow,rowin in enumerate(rows):
  (key1,lnum,line) = rowin
  # replace lnum with sequence number, and make it a string
  newlnum = str(irow + 1)
  row = (key1,newlnum,line)
  if len(batch) < mbatch:
   # add row to batch
   batch.append(row)
  else:
   # insert records of (full) batch, and commit?
   insert_batch(c,conn,dictlo,batch)
   # reinit batch
   batch = []
   # add this row to batch
   batch.append(row)
%else:
 nrow = len(lines)
 batch = []
 for line0 in lines:
  line = line0.rstrip('\r\n')
  if not line.startswith('<H'):
   continue
  m = re.search(r'<key1>(.*?)</key1>.*<L>(.*?)</L>',line)
  if not m:
   print('ERROR: Could not find key1,lnum from line: %s' %line)
   exit(1)
  key1 = m.group(1)
  lnum = m.group(2)
  row = (key1,lnum,line)
  if len(batch) < mbatch:
   # add row to batch
   batch.append(row)
  else:
   # insert records of (full) batch, and commit?
   insert_batch(c,conn,dictlo,batch)
   # reinit batch
   batch = []
   # add this row to batch
   batch.append(row)
%endif

 # insert last batch
 insert_batch(c,conn,dictlo,batch)
 # create index
 create_index(c,conn,dictlo)
 conn.close()  # close the connection to xxx.sqlite
 time1 = time.time()  # ending time
 print(nrow,'rows written to',fileout)
 timediff = time1 - time0 # seconds
 print('%0.2f seconds for batch size %s' %(timediff,mbatch))
