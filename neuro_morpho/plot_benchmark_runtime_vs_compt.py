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

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

dbpath = os.path.join('.', '_profile.sqlite')
db = sql.connect(dbpath)
db.row_factory = dict_factory

curr = db.cursor()

def getMOOSE():
    query = """SELECT * FROM table201507 WHERE
    simulator='moose' ORDER BY number_of_compartments"""
    result = []
    for row in curr.execute(query):
        result.append(row)

    header = ['number_of_compartments'
            , 'number_of_channels'
            , 'run_time'
            , 'dt'
            , 'number_of_spikes'
            , 'mean_spike_interval'
            , 'variance_spike_interval'
            ]
    with open('moose_performance.csv', "w") as f:
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
        

def getNRN():
    pass

def main():
    moose = getMOOSE()
    nrn = getNRN()

if __name__ == '__main__':
    main()
