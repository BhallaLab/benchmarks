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


def main():
    db = sql.connect(_profile.dbFile)
    models = []
    query="SELECT model_name from %s WHERE simulator='neuron'" % _profile.tableName
    for e in db.execute(query):
        models.append(e[0])
    for mod in models:
        query = """SELECT * FROM {} WHERE model_name='{}' AND simulator='{}'"""
        neurons = db.execute(query.format(_profile.tableName, mod, 'neuron'))
        mooses = db.execute(query.format(_profile.tableName, mod, 'moose'))
        print neurons.fetchall()
        print mooses.fetchall()
        print "====="


if __name__ == '__main__':
    main()
