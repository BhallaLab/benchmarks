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
compartment_size_limit = 2000

# No of compartments for neuron are less by a factor of

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db = sql.connect(_profile.dbFile)
db.row_factory = dict_factory

def rowCompare(mooseData, nrnData):
    """Since moose runtime scales linearly, in this comparision we scale moose
    time according to compartments created in neurons.
    """

    # Time taken for 1 unit time simulation. 
    mooseRunTime = np.mean([ x['run_time'] / x['simulation_time'] for x in mooseData])
    nrnRunTime = np.mean([ 1000 * x['run_time'] / x['simulation_time'] for x in nrnData])

    mooseCompts = np.mean([x['number_of_compartments'] for x in mooseData])
    nrnCompts = np.mean([x['number_of_compartments'] for x in nrnData])
    nrnScale = mooseCompts / float(nrnCompts)
    return nrnCompts, mooseRunTime / nrnScale, nrnRunTime


def plot_with_models_on_x_axis():
    global db
    models = []
    query="SELECT model_name from %s WHERE simulator='neuron'" % _profile.tableName
    for e in db.execute(query):
        models.append(e['model_name'])

    mooseDict = defaultdict(list)
    nrnDict = defaultdict(list)
    segDict = {}

    xvec = []
    for mod in models:
        query = """SELECT * FROM {} WHERE model_name='{}' AND simulator='{}'"""
        #AND timestamp > date('now', '{}')"""
        neurons = db.execute(query.format(_profile.tableName, mod, 'neuron'))
        for n in neurons.fetchall():
            nrnDict[mod].append(n)

        mooses = db.execute(query.format(_profile.tableName, mod, 'moose'))
        for m in mooses.fetchall():
            mooseDict[mod].append(m)

    print("Total %s entries found for moose" % len(mooseDict))
    print("Total %s entries found for nrn" % len(nrnDict))

    # for each model in mooose, compare it with neuron.
    nrnVec = []
    mooseVec = []
    segVec = []
    
    print("NOTICE: Compartment size limit : %s" % compartment_size_limit)
    for i, k in enumerate(mooseDict):
        xvec.append(k)
        mooseData = mooseDict[k]
        nrnData = nrnDict[k]
        nrnseg, mooseTime, nrnTime = rowCompare(mooseData, nrnData)
        if nrnseg < compartment_size_limit:
            segVec.append(nrnseg)
            segDict[k] = nrnseg
            nrnVec.append(nrnTime)
            mooseVec.append(mooseTime)

    print("[INFO] Writing to %s" % "nrn_moose_compare_1_sec.csv")
    with open("nrn_moose_compare_1_sec.csv", "w") as f:
        f.write("compartments,neuron,moose\n")
        for i, s in enumerate(segVec):
            line = "%s,%s,%s\n" % (s, nrnVec[i], mooseVec[i])
            f.write(line)

    pylab.plot(segVec, nrnVec, '.', label="Neuron")
    pylab.plot(segVec, mooseVec, '*', label="MOOSE")
    pylab.legend(loc='best', framealpha=0.4)
    pylab.title("MOOSE Vs NEURON")
    pylab.xlabel("No of compartments")
    pylab.ylabel("Run time for 1 sec simulation")
    outfile = '_plots/moose_vs_neuron_compt_x_axis.png'
    print("[INFO] Saving to %s" % outfile)
    pylab.savefig(outfile)

def compareMOOSEAndNEURON():
    print("++ Comparing MOOSE and NEURON")



def main():
    #compareMOOSEAndNEURON()
    plot_with_models_on_x_axis()
    
if __name__ == '__main__':
    main()
