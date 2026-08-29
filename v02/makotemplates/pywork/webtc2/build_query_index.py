# coding=utf-8
""" build_query_index.py
 Build the generation-time SQLite line index (query_dump.sqlite3) that
 webtc2/querymodel.php consults instead of linearly fgets-scanning the whole
 query_dump.txt on every request (H3487 audit finding W10, prior audit D4).

 The flat file remains the source of truth.  The index only narrows which
 lines PHP examines; querymodel.php still re-applies its exact legacy regex
 match per candidate line, so results are identical to the plain scan.

 Schema (deliberately simple, parity-safe):
   PRAGMA user_version = 1           -- schema marker checked by querymodel.php
   meta(k TEXT PRIMARY KEY, v TEXT)  -- 'dumpsize': byte size of the dump this
                                        index was built from; querymodel.php
                                        refuses (falls back to the scan) an
                                        index that does not match the dump
   lines(off INTEGER PRIMARY KEY,    -- byte offset of the line start in the
                                        dump; usable directly with fseek()
        t TEXT)                      -- the line, trailing newline stripped
                                        and '-' removed (querymodel matches
                                        against the hyphen-stripped line,
                                        COLOGNE#75)
"""
from __future__ import print_function

import os
import sqlite3
import sys

SCHEMA_VERSION = 1
BATCH = 20000


def build(filein, fileout):
  if os.path.exists(fileout):
    os.remove(fileout)
  dumpsize = os.path.getsize(filein)
  con = sqlite3.connect(fileout)
  cur = con.cursor()
  cur.execute('PRAGMA user_version = %d' % SCHEMA_VERSION)
  cur.execute('CREATE TABLE meta(k TEXT PRIMARY KEY, v TEXT)')
  cur.execute('CREATE TABLE lines(off INTEGER PRIMARY KEY, t TEXT)')
  cur.execute("INSERT INTO meta VALUES('dumpsize',?)", (str(dumpsize),))
  off = 0
  batch = []
  # newline='' : keep '\r\n' verbatim so 'off' counts real file bytes
  with open(filein, encoding='utf-8', newline='') as f:
    for line in f:
      t = line.rstrip('\r\n').replace('-', '')
      batch.append((off, t))
      off = off + len(line.encode('utf-8'))
      if len(batch) >= BATCH:
        cur.executemany('INSERT INTO lines VALUES(?,?)', batch)
        batch = []
  if batch:
    cur.executemany('INSERT INTO lines VALUES(?,?)', batch)
  con.commit()
  n = cur.execute('SELECT count(*) FROM lines').fetchone()[0]
  cur.close()
  con.close()
  return n


def main():
  filein = sys.argv[1]  # query_dump.txt
  fileout = sys.argv[2]  # query_dump.sqlite3
  n = build(filein, fileout)
  print(n, "lines indexed from", filein)
  print("index written to", fileout)


if __name__ == "__main__":
  main()
