#!/usr/bin/env python

"""plot_benchmark_runtime_vs_compt.py: 

    Plot benchmark.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import os
import sys
import sqlite3 as sql 
import time

month = time.strftime("%Y%m")
tableName = 'table%s' % month
print("Selecting table: %s" % tableName)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

dbpath = os.path.join('.', '_profile.sqlite')
db = sql.connect(dbpath)
db.row_factory = dict_factory

curr = db.cursor()

def compare(simA, simB):
    pass

def getSIM(simname = 'moose'):
    query = """SELECT * FROM {0} WHERE
    simulator='{1}' ORDER BY number_of_compartments""".format(tableName, simname)
    result = []
    for row in curr.execute(query):
        result.append(row)

    header = ['number_of_compartments'
            , 'number_of_channels'
            , 'run_time'
            , 'simulation_time'
            , 'dt'
            , 'number_of_spikes'
            , 'mean_spike_interval'
            , 'variance_spike_interval'
            ]
    csvFile = "%s_performance.csv" % simname
    print("[INFO] Writing to %s" % csvFile)
    with open(csvFile, "w") as f:
        f.write("{}\n".format(",".join(header)))
        for r in result:
            line = []
            for h in header:
                try:
                    line.append('%s' % r[h])
                except:
                    print("Key %s not found" % h)
                    print(r.keys())
            f.write("{}\n".format(",".join(line)))
    return result
     
def getMOOSE():
    return getSIM('moose')

def getNRN():
    return getSIM('neuron')

def main():
    moose = getMOOSE()
    nrn = getNRN()
    compare(nrn, moose)

if __name__ == '__main__':
    main()
