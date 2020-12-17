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
 template = '''
CREATE TABLE %s (
 key VARCHAR(100)  NOT NULL,
 lnum DECIMAL(10,2) UNIQUE,
 data TEXT NOT NULL
);
  ''' % dictlo
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
 
 f = codecs.open(filein,"r","utf-8")
 nlines = 0
 nrow = 0
 batch = []
 for line0 in f:
  nlines = nlines + 1
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
   nrow = nrow + 1
  else:
   # insert records of (full) batch, and commit?
   insert_batch(c,conn,dictlo,batch)
   # reinit batch
   batch = []
   # add this row to batch
   batch.append(row)
   nrow = nrow + 1
 f.close()
 # insert last batch
 insert_batch(c,conn,dictlo,batch)
 # create index
 create_index(c,conn,dictlo)
 conn.close()  # close the connection to xxx.sqlite
 time1 = time.time()  # ending time
 print(nlines,'lines read from',filein)
 print(nrow,'rows written to',fileout)
 timediff = time1 - time0 # seconds
 print('%0.2f seconds for batch size %s' %(timediff,mbatch))
