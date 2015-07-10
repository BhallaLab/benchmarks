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

ignore_before = "-10 days"
# No of compartments for neuron are less by a factor of

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db = sql.connect(_profile.dbFile)
db.row_factory = dict_factory

def compare(mooseData, nrnData):
    mooseRunTime = np.mean([ x['run_time'] for x in mooseData])
    nrnRunTime = np.mean([ x['run_time'] for x in nrnData])
    print mooseRunTime, nrnRunTime




def plot_with_models_on_x_axis():
    global db
    models = []
    query="SELECT model_name from %s WHERE simulator='neuron'" % _profile.tableName
    for e in db.execute(query):
        models.append(e['model_name'])

    mooseDict = defaultdict(list)
    nrnDict = defaultdict(list)

    for mod in models:
        query = """SELECT * FROM {} WHERE model_name='{}' AND simulator='{}'"""
        #AND timestamp > date('now', '{}')"""
        neurons = db.execute(query.format(_profile.tableName, mod, 'neuron'))
        for n in neurons.fetchall():
            nrnDict[mod].append(n)

        mooses = db.execute(query.format(_profile.tableName, mod, 'moose'))
        for m in mooses.fetchall():
            mooseDict[mod].append(n)

    print("Total %s entries found for moose" % len(mooseDict))
    print("Total %s entries found for nrn" % len(nrnDict))

    # for each model in mooose, compare it with neuron.
    for k in mooseDict:
        mooseData = mooseDict[k]
        nrnData = nrnDict[k]
        compare(mooseData, nrnData)

    #width = 0.3
    #rect1 = pylab.bar(np.arange(len(xvec)), nrnVec, width, color='b'
            #, label='neuron')
    #rect2 = pylab.bar(np.arange(len(xvec))+width, mooseVec, width, color='r'
            #, label='moose')
    #pylab.legend(loc='best', framealpha=0.4)
    #pylab.savefig('benchmark_model_name_of_x_axis.png')


def compareMOOSEAndNEURON():
    print("++ Comparing MOOSE and NEURON")



def main():
    #compareMOOSEAndNEURON()
    plot_with_models_on_x_axis()
    
if __name__ == '__main__':
    main()
