"""sqlite_txt.py
Create xxx.sqlite from tab-separated input files.
Replaces: sqlite3 xxx.sqlite < xxx.sql
"""
from __future__ import print_function
import sys, re, os, sqlite3, time

SCHEMA_MAP = {
    'stcab': [
        '`id` VARCHAR(100)  UNIQUE',
        '`data` TEXT  NOT NULL',
    ],
    'mwab': [
        '`id` VARCHAR(100)  UNIQUE',
        '`data` TEXT  NOT NULL',
    ],
    'pwab': [
        '`id` VARCHAR(100)  UNIQUE',
        '`data` TEXT  NOT NULL',
    ],
    'benab': [
        '`id` VARCHAR(100)  UNIQUE',
        '`data` TEXT  NOT NULL',
    ],
    'apab': [
        '`id` VARCHAR(100)  UNIQUE',
        '`data` TEXT  NOT NULL',
    ],
    'caeab': [
        '`id` VARCHAR(100)  UNIQUE',
        '`data` TEXT  NOT NULL',
    ],
    'burab': [
        '`id` VARCHAR(100)  UNIQUE',
        '`data` TEXT  NOT NULL',
    ],
    'bhsab': [
        '`id` VARCHAR(100)  UNIQUE',
        '`data` TEXT  NOT NULL',
    ],
    'graab': [
        '`id` VARCHAR(100)  UNIQUE',
        '`data` TEXT  NOT NULL',
    ],
    'lanab': [
        '`id` VARCHAR(100)  UNIQUE',
        '`data` TEXT  NOT NULL',
    ],
    'mdab': [
        '`id` VARCHAR(100)  UNIQUE',
        '`data` TEXT  NOT NULL',
    ],
    'pwgab': [
        '`id` VARCHAR(100)  UNIQUE',
        '`data` TEXT  NOT NULL',
    ],
    'pwkvnab': [
        '`id` VARCHAR(100)  UNIQUE',
        '`data` TEXT  NOT NULL',
    ],
    'ap90ab': [
        '`id` VARCHAR(100)  UNIQUE',
        '`data` TEXT  NOT NULL',
    ],
    'apauthtooltips': [
        '`key` VARCHAR(20) NOT NULL',
        '`data` VARCHAR(20000) NOT NULL',
    ],
    'schauthtooltips': [
        '`key` VARCHAR(20) NOT NULL',
        '`data` VARCHAR(20000) NOT NULL',
    ],
    'graauthtooltips': [
        '`key` VARCHAR(20) NOT NULL',
        '`data` VARCHAR(20000) NOT NULL',
    ],
    'benauthtooltips': [
        '`key` VARCHAR(20) NOT NULL',
        '`data` VARCHAR(20000) NOT NULL',
    ],
    'bhsauthtooltips': [
        '`key` VARCHAR(20) NOT NULL',
        '`data` VARCHAR(20000) NOT NULL',
    ],
    'ap90authtooltips': [
        '`key` VARCHAR(20) NOT NULL',
        '`data` VARCHAR(20000) NOT NULL',
    ],
    'pwbib': [
        '`id` VARCHAR(100)  UNIQUE',
        '`code` TEXT',
        '`codecap` TEXT',
        '`data` TEXT  NOT NULL',
    ],
    'pwgbib': [
        '`id` VARCHAR(100)  UNIQUE',
        '`code` TEXT',
        '`codecap` TEXT',
        '`data` TEXT  NOT NULL',
    ],
    'pwkvnbib': [
        '`id` VARCHAR(100)  UNIQUE',
        '`code` TEXT',
        '`codecap` TEXT',
        '`data` TEXT  NOT NULL',
    ],
    'mwauthtooltips': [
        '`cid` VARCHAR(20) NOT NULL',
        '`key` VARCHAR(20) NOT NULL',
        '`data` VARCHAR(20000) NOT NULL',
        '`type` VARCHAR(20) NOT NULL',
    ],
    'mwkeys': [
        'key VARCHAR(100)  NOT NULL',
        'lnum DECIMAL(10,2) UNIQUE',
        'data TEXT NOT NULL',
    ],
    'westmwtab': [
        'key VARCHAR(100)  NOT NULL',
        'lnum DECIMAL(10,2) NOT NULL',
        'data TEXT NOT NULL',
    ],
    'whitmwtab': [
        'key VARCHAR(100)  NOT NULL',
        'lnum DECIMAL(10,2) NOT NULL',
        'data TEXT NOT NULL',
    ],
}

NO_INDEX_TABLES = {
    'westmwtab', 'whitmwtab',
    'apauthtooltips', 'schauthtooltips', 'graauthtooltips',
    'benauthtooltips', 'bhsauthtooltips', 'ap90authtooltips',
    'mwauthtooltips',
}


def remove(fileout):
    if os.path.exists(fileout):
        os.remove(fileout)
        print('removed previous', fileout)


def create_table(c, conn, tabname, columns):
    template = 'CREATE TABLE %s (\n %s\n);' % (tabname, ',\n '.join(columns))
    c.execute(template)
    conn.commit()


def create_index(c, conn, tabname, columns):
    time0 = time.time()
    colname = columns[0].split()[0].strip('`')
    c.execute('CREATE INDEX datum on %s(%s)' % (tabname, colname))
    conn.commit()
    c.execute('pragma table_info (%s)' % tabname)
    c.execute('select count(*) from %s' % tabname)
    result = c.fetchone()
    if result:
        print(result[0])
    time1 = time.time()
    print('create_index takes %0.2f seconds' % (time1 - time0))


def insert_rows(c, conn, tabname, rows):
    if len(rows) == 0:
        return
    placeholders = ','.join(['?'] * len(rows[0]))
    sql = 'INSERT INTO %s VALUES (%s)' % (tabname, placeholders)
    c.executemany(sql, rows)
    conn.commit()


if __name__ == '__main__':
    time0 = time.time()

    filein = sys.argv[1]
    fileout = sys.argv[2]
    tabname = sys.argv[3]

    if tabname not in SCHEMA_MAP:
        print('sqlite_txt.py ERROR: unknown table name:', tabname)
        print('Known tables:', ', '.join(sorted(SCHEMA_MAP.keys())))
        sys.exit(1)

    columns = SCHEMA_MAP[tabname]
    num_cols = len(columns)

    remove(fileout)
    conn = sqlite3.connect(fileout)
    c = conn.cursor()
    create_table(c, conn, tabname, columns)

    with open(filein, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\r\n') for line in f]
    print(len(lines), 'lines read from', filein)

    nrow = 0
    rows = []
    for line in lines:
        parts = line.split('\t')
        if len(parts) != num_cols:
            print('WARNING: expected %d columns, got %d in line: %s' % (num_cols, len(parts), line))
            continue
        rows.append(tuple(parts))

    insert_rows(c, conn, tabname, rows)
    nrow = len(rows)

    if tabname not in NO_INDEX_TABLES:
        create_index(c, conn, tabname, columns)

    conn.close()
    print(nrow, 'rows written to', fileout)
    time1 = time.time()
    print('%0.2f seconds' % (time1 - time0))
