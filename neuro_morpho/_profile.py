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
import pprint as pp

uname_ = platform.uname()

dbFile = '_profile.sqlite'
conn_ = sql.connect(dbFile)
cur_ = conn_.cursor()

import time
month = time.strftime("%Y%m")
print month
tableName = 'table%s' % month

cur_.execute(
        """CREATE TABLE IF NOT EXISTS {} (
        timestamp DATETIME 
        , model_name VARCHAR
        , number_of_compartments INTEGER 
        , number_of_channels INTEGER
        , simulator TEXT NOT NULL
        , simulation_time REAL DEFAULT 0
        , run_time REAL DEFAULT 0
        , dt REAL DEFAULT 0.000000001
        , number_of_spikes INTEGER
        , mean_spike_interval REAL
        , variance_spike_interval REAL
        , comment TEXT
        , uname TEXT DEFAULT "{}"
        )""".format(tableName, uname_)
        )

def dbEntry(queryDict):
    keys = []
    vals = []
    for k in queryDict: 
        keys.append(k)
        try:
            vals.append("'%s'" % queryDict[k])
        except Exception as e:
            print(queryDict[k])
            raise Exception
    keys.append("timestamp")
    vals.append("datetime('now')")
    keys = ",".join(keys)
    vals = ",".join(vals)
    query = """INSERT INTO {} ({}) VALUES ({})""".format(tableName, keys, vals)
    pp.pprint(queryDict)
    cur_.execute(query)
    conn_.commit()

def main():
    print("No tests")
    pass

if __name__ == '__main__':
    main()
