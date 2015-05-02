#!/usr/bin/env python
"""plot_benchmark.py: 

Plot the benchmarks.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import _profile 
import sqlite3 as sql
from collections import defaultdict

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db = sql.connect(_profile.dbFile)
db.row_factory = dict_factory

def main():
    global db
    models = []
    query="SELECT model_name from %s WHERE simulator='neuron'" % _profile.tableName
    for e in db.execute(query):
        models.append(e['model_name'])

    mooseDict = defaultdict(list)
    nrnDict = defaultdict(list)

    for mod in models:
        query = """SELECT * FROM {} WHERE model_name='{}' AND simulator='{}'"""
        neurons = db.execute(query.format(_profile.tableName, mod, 'neuron'))
        mooses = db.execute(query.format(_profile.tableName, mod, 'moose'))
        for n in neurons.fetchall():
            nrnDict[mod].append(n['runtime']/n['simtime'])
        for m in mooses.fetchall():
            mooseDict[mod].append(m['runtime']/m['simtime'])

    for k in mooseDict:
        print mooseDict[k]
        print nrnDict[k]


if __name__ == '__main__':
    main()