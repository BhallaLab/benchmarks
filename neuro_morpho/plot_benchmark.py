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
import numpy as np
import pylab
from collections import defaultdict

ignore_before = "-10 hours"
# No of compartments for neuron are less by a factor of

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db = sql.connect(_profile.dbFile)
db.row_factory = dict_factory

def plot_with_models_on_x_axis():
    global db
    models = []
    query="SELECT model_name from %s WHERE simulator='neuron'" % _profile.tableName
    for e in db.execute(query):
        models.append(e['model_name'])

    mooseDict = defaultdict(list)
    nrnDict = defaultdict(list)
    secDict = {}

    for mod in models:
        query = """SELECT * FROM {} WHERE model_name='{}' AND simulator='{}'
        AND time > date('now', '{}')"""
        neurons = db.execute(query.format(_profile.tableName, mod, 'neuron',
            ignore_before))
        mooses = db.execute(query.format(_profile.tableName, mod, 'moose',
            ignore_before))
        for n in neurons.fetchall():
            nrnDict[mod].append(n['runtime']/n['simtime'])
        for m in mooses.fetchall():
            mooseDict[mod].append(m['runtime']/m['simtime'])
            secDict[mod] = n['no_of_compartments']

    nrnVec = []
    mooseVec = []
    xvec = []
    for k in mooseDict:
        mooseVec.append(np.mean(mooseDict[k]))
        nrnVec.append(nrn_scale * np.mean(nrnDict[k]))
        xvec.append(secDict[k])

    width = 0.3
    rect1 = pylab.bar(np.arange(len(xvec)), nrnVec, width, color='b'
            , label='neuron')
    rect2 = pylab.bar(np.arange(len(xvec))+width, mooseVec, width, color='r'
            , label='moose')
    pylab.legend(loc='best', framealpha=0.4)
    pylab.savefig('benchmark_model_name_of_x_axis.png')


def compareMOOSEAndNEURON():
    print("++ Comparing MOOSE and NEURON")



def main():
    compareMOOSEAndNEURON()
    
if __name__ == '__main__':
    main()
