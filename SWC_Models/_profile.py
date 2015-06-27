"""config.py: 

    Global variables.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sqlite3 as sql 
import sys
import platform
import logging

uname_ = platform.uname()

dbFile = '_profile.sqlite'
conn_ = sql.connect(dbFile)
cur_ = conn_.cursor()
tableName = 'swc'

cur_.execute(
        """CREATE TABLE IF NOT EXISTS {} ( time DATETIME 
        , model_name VARCHAR
        , no_of_compartments INTEGER 
        , no_of_channels INTEGER
        , simulator TEXT NOT NULL
        , simtime REAL DEFAULT 0
        , runtime REAL DEFAULT 0
        , dt REAL DEFAULT 0.000000001
        , comment TEXT
        , uname TEXT DEFAULT "{}"
        )""".format(tableName, uname_)
        )

def dbEntry(**values):
    keys = []
    vals = []
    for k in values: 
        keys.append(k)
        try:
            vals.append("'%s'" % values[k])
        except Exception as e:
            print(values[k])
            raise Exception
    keys.append("time")
    vals.append("datetime('now')")

    keys = ",".join(keys)
    vals = ",".join(vals)
    
    query = """INSERT INTO {} ({}) VALUES ({})""".format(tableName, keys, vals)
    print("Excuting: %s" % query)
    cur_.execute(query)
    conn_.commit()

def main():
    dbEntry({ 'no_of_compartment': 100, 'coretime' : 0.0001, 'simulator' : 'moose' })
    dbEntry({ 'no_of_compartment': 100, 'coretime' : 0.0001, 'simulator' : 'neuron' })
    for c in cur_.execute("SELECT * from %s"%tableName):
        print c

if __name__ == '__main__':
    main()
